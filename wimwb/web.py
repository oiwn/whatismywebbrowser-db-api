from typing import List

import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseSettings
from sqlalchemy.orm import sessionmaker
from sqlalchemy.sql.expression import func

from wimwb.schemas import UserAgentShort
from wimwb.models import WhatismybrowserUseragent


class Settings(BaseSettings):
    """Application settings"""

    app_name: str = "Whatismywebbrowser database API"
    database_uri: str

    class Config:  # pylint: disable=too-few-public-methods
        """Automatically load settings from .env file"""

        env_file = ".env"
        env_file_encoding = "utf-8"


# setup things
settings = Settings()
database = databases.Database(settings.database_uri)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(settings.database_uri)
user_agents = WhatismybrowserUseragent.__table__  # pylint: disable=no-member

# setup application
app = FastAPI()


@app.on_event("startup")
async def startup():
    """Create connection to database at startup"""
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    """Close connection to database at startup"""
    await database.disconnect()


@app.get("/user-agents/", response_model=List[UserAgentShort])
async def random_user_agents(limit: int = 5):
    """Return random user agents"""
    query = user_agents.select().order_by(func.rand()).limit(limit)
    rows = await database.fetch_all(query=query)
    return rows
