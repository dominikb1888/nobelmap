from contextlib import asynccontextmanager
from typing import Union
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from sqlmodel import Session, select
from db import create_db_and_tables, engine
from models import NobelWinner, Address, Organization


@asynccontextmanager
async def lifespan(app: FastAPI):
    create_db_and_tables()
    yield


app = FastAPI(lifespan=lifespan)
app.mount("/static", StaticFiles(directory="static"), name="static")
templates = Jinja2Templates(directory="templates")


@app.get("/", response_class=HTMLResponse)
def index(request: Request):
    with Session(engine) as session:
        # add code to get view from DB
        data = session.exec(select(Address.country).distinct()).all()
        return templates.TemplateResponse(
            "index.html", {"request": request, "data": data}
        )


@app.get("/data/", response_class=JSONResponse, response_model=list)
def read_data():
    with Session(engine) as session:
        data = session.exec(
            select(NobelWinner).join(Organization).join(Address).distinct()
        ).all()
        return data


@app.post("/nobelwinners/", response_class=JSONResponse)
def create_nobelwinners(nobelwinner: NobelWinner):
    with Session(engine) as session:
        session.add(nobelwinner)
        session.commit()
        session.refresh(nobelwinner)
        return nobelwinner


@app.get(
    "/nobelwinners/", response_class=JSONResponse, response_model=list[NobelWinner]
)
def read_nobelwinners():
    with Session(engine) as session:
        nobelwinners = session.exec(select(NobelWinner)).all()
        return nobelwinners


app.post("/addresses/", response_class=JSONResponse)


def create_addresses(addresses: Address):
    with Session(engine) as session:
        session.add(addresses)
        session.commit()
        session.refresh(addresses)
        return addresses


@app.get("/addresses/", response_class=JSONResponse, response_model=list[Address])
def read_addresses():
    with Session(engine) as session:
        addresses = session.exec(select(Address)).all()
        return addresses


@app.post("/organizations/", response_class=JSONResponse)
def create_organizations(addresses: Organization):
    with Session(engine) as session:
        session.add(addresses)
        session.commit()
        session.refresh(addresses)
        return addresses


@app.get("/addresses/", response_class=JSONResponse, response_model=list[Address])
def read_organizations():
    with Session(engine) as session:
        organizatuions = session.exec(select(Organization)).all()
        return organizations
