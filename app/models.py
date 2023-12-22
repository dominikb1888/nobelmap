from datetime import date
from typing import Optional

from geojson_pydantic import Point
from pydantic_extra_types.country import CountryInfo
from sqlmodel import SQLModel, Column, Field, JSON
from sqlmodel.main import Relationship


class Address(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    address_type: Optional[str] = None
    street: Optional[str] = None
    zip: Optional[str] = None
    city: Optional[str] = None
    country: Optional[CountryInfo] = Field(
        sa_column=Column(JSON), default={"all": "true"}
    )
    coordinates: Optional[Point] = Field(
        sa_column=Column(JSON), default={"all": "true"}
    )
    person_id: Optional[int] = Field(default=None, foreign_key="nobelwinner.id")
    winner: Optional["NobelWinner"] = Relationship(back_populates="address")
    orgaddress: Optional["Organization"] = Relationship(back_populates="address")


class Organization(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    name: Optional[str] = None
    category: Optional[str] = None
    address_id: Optional[int] = Field(default=None, foreign_key="address.id")
    winner: Optional["NobelWinner"] = Relationship(back_populates="org")
    address: Optional[list[Address]] = Relationship(back_populates="orgaddress")


class NobelWinner(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    firstname: Optional[str] = None
    surname: Optional[str] = None
    born: Optional[date] = None
    died: Optional[date] = None
    gender: Optional[str] = None
    year: Optional[int] = None
    category: Optional[str] = None
    overallmotivation: Optional[str] = None
    motivation: Optional[str] = None
    org_id: Optional[int] = Field(default=None, foreign_key="organization.id")
    org: Optional[Organization] = Relationship(back_populates="winner")
    address: Optional[list[Address]] = Relationship(back_populates="winner")
