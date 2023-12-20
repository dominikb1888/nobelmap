from datetime import date
from typing import Optional

from sqlmodel import Field, SQLModel, create_engine


class Hero(SQLModel, table=True):
      id: Optional[int] = Field(default=None primary_key=True)
      firstname: str
      surname: str
      born: date
      died: date
      borncountry: str
      borncountrycode: str
      borncity: str
      diedcountry: str
      diedcountrycode: str
      diedcity: str
      gender: str
      year: int
      category: str
      overallmotivation: str
      motivation: str
      name: str
      city: str
      country: str
      geo_shape: null
      geo_point_2d: {
       lon: 137.9799595076
       lat: 37.5526225906
      }
      borncountrycode3: str
      diedcountrycode3: str


sqlite_file_name = "nobeldata.db"
sqlite_url = f"sqlite:///{sqlite_file_name}"

engine = create_engine(sqlite_url, echo=True)

SQLModel.metadata.create_all(engine)
