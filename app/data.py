import json
from datetime import datetime
import pycountry

from sqlmodel import Session
from db import engine
from models import NobelWinner, Address, Organization
from geojson_pydantic import Feature, Point

CMAP = {
    "the Netherlands": "Netherlands",
    "USSR (now Russia)": "Russian Federation",
    "Czechoslovakia (now Czech Republic)": "Czechia",
    "Russia": "Russian Federation",
    "Germany (now France)": "France",
    "USA": "United States",
}


class ImportData:
    def __init__(self, filepath: str):
        self.data = self.get_data(filepath)
        self.countrycodes = self.get_countrycodes()
        self.countries = self.create_countries()

    @staticmethod
    def get_data(filepath: str) -> list[dict]:
        with open(filepath) as f:
            data = json.load(f)

        return data

    def get_countrycodes(self) -> set:
        labels = ["borncountrycode", "diedcountrycode"]
        countries_person = {
            item[label] for item in self.data for label in labels if item[label]
        }
        countries_org = self.get_org_countrycodes()
        return countries_person | countries_org

    def lookup_code(self, countrycode: str):
        try:
            if countrycode:
                country = pycountry.countries.get(alpha_2=countrycode)
                return country

        except LookupError:
            print(f"Alpha-2 Countrycode {countrycode} not found")

    def lookup_name(self, countryname: str):
        try:
            if countryname:
                country = pycountry.countries.get(name=countryname)
                return country if country else countryname

        except LookupError:
            print(f"Country {countryname} not found")

    def create_countries(self) -> list:
        print(self.countrycodes)
        return [self.lookup_code(countrycode) for countrycode in self.countrycodes]

    def get_country_from_name(self, countryname) -> set:
        country = CMAP.get(countryname, countryname)
        if country:
            pycountry = self.lookup_name(country)
            if pycountry:
                return pycountry
            else:
                raise LookupError(f"Countryname {countryname} not found")

    def get_org_countrycodes(self) -> set:
        names = set()
        for item in self.data:
            country = CMAP.get(item["country"], item["country"])
            pycountry = self.lookup_name(country)
            if pycountry:
                names.add(pycountry.alpha_2)

        return names

    def create_organization(self, item: dict, fields: list, id: int) -> Organization:
        with Session(engine) as session:
            organization = Organization(name=item["name"], category="", person_id=id)
            session.add(organization)
            session.commit()
            session.refresh(organization)
            self.create_address(item, fields, id=organization.id)
            return organization.id

    def create_address(self, item: dict, fields: list, id: int) -> Address:
        with Session(engine) as session:
            city = next(
                item[field]
                for field in fields
                if field in ["borncity", "diedcity", "city"]
            )
            if "country" in fields:
                country = self.get_country_from_name(item["country"])
            else:
                code = next(
                    item[field]
                    for field in fields
                    if field in ["borncountrycode", "diedcountrycode"]
                )
                country = self.lookup_code(code)

            coordinates = Point(coordinates=(0, 0), type="Point")
            if ("geo_point_2d" in fields) and item["geo_point_2d"]:
                lon, lat = item["geo_point_2d"].values()
                coordinates.coordinates = (lon, lat)

            addict = {
                "city": city,
                "country": country.__dict__ if country else None,
                "coordinates": coordinates.__dict__,
            }

            if "borncountry" in fields:
                addict["born_id"] = id
            if "diedcountry" in fields:
                addict["died_id"] = id
            if "country" in fields:
                addict["org_id"] = id

            address = Address(**addict)

            session.add(address)
            session.commit()
            session.refresh(address)
            return address.id

    def populate_db(self):
        with Session(engine) as session:
            for item in self.data:
                nobelwinner_fields = [
                    "firstname",
                    "surname",
                    "born",
                    "died",
                    "gender",
                    "year",
                    "category",
                ]
                filtered_item = {
                    k: v for k, v in item.items() if k in nobelwinner_fields
                }
                print(filtered_item)
                if filtered_item["born"]:
                    filtered_item["born"] = datetime.strptime(
                        filtered_item["born"], "%Y-%m-%d"
                    )

                if filtered_item["died"]:
                    filtered_item["died"] = datetime.strptime(
                        filtered_item["died"], "%Y-%m-%d"
                    )
                nobelwinner = NobelWinner(**filtered_item)
                bornaddress_fields = ["borncountrycode", "borncity"]
                diedaddress_fields = ["diedcountrycode", "diedcity"]
                orgaddress_fields = ["name", "city", "country", "geo_point_2d"]

                session.add(nobelwinner)
                session.commit()
                session.refresh(nobelwinner)

                self.create_address(item, bornaddress_fields, id=nobelwinner.id)
                self.create_address(item, diedaddress_fields, id=nobelwinner.id)
                self.create_organization(item, orgaddress_fields, id=nobelwinner.id)

                print("New Nobelwinner added:", nobelwinner)


data = ImportData("nobellaureates.json")
data.populate_db()
# {
#   "id": 351,
#   "firstname": "Philip S.",
#   "surname": "Hench",
#   "born": "1896-02-28",
#   "died": "1965-03-30",
#   "borncountry": "USA",
#   "borncountrycode": "US",
#   "borncity": "Pittsburgh PA",
#   "diedcountry": "Jamaica",
#   "diedcountrycode": "JM",
#   "diedcity": "Ocho Rios",
#   "gender": "male",
#   "year": 1950,
#   "category": "Medicine",
#   "overallmotivation": null,
#   "motivation": "\"for their discoveries relating to the hormones of the adrenal cortex their structure and biological effects\"",
#   "name": "Mayo Clinic",
#   "city": "Rochester MN",
#   "country": "USA",
#   "geo_shape": null,
#   "geo_point_2d": {
#     "lon": -112.4943339159,
#     "lat": 45.6875333395
#   },
#   "borncountrycode3": "USA",
#   "diedcountrycode3": "JAM"
# }
