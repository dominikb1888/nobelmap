from datetime import date
from typing import Optional

from geojson_pydantic import Point
from pydantic_extra_types.country import CountryInfo
from sqlmodel import Field, Relationship, SQLModel, Column, JSON


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    street: Optional[str]
    zip: Optional[str]
    city: Optional[str]
    country: Optional[CountryInfo] = Field(
        sa_column=Column(JSON), default={"all": "true"}
    )
    coordinates: Optional[Point] = Field(
        sa_column=Column(JSON), default={"all": "true"}
    )
    born_id: Optional[int] = Field(default=None, foreign_key="nobelwinner.id")
    died_id: Optional[int] = Field(default=None, foreign_key="nobelwinner.id")
    org_id: Optional[int] = Field(default=None, foreign_key="organization.id")


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str]
    category: Optional[str]
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")
    person_id: Optional[int] = Field(default=None, foreign_key="nobelwinner.id")


class NobelWinner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: Optional[str]
    surname: Optional[str]
    born: Optional[date]
    died: Optional[date]
    gender: Optional[str]
    year: Optional[int]
    category: Optional[int]
    overallmotivation: Optional[int]
    motivation: Optional[int]
