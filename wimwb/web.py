import os
from typing import List

import databases
import sqlalchemy
from pydantic import BaseSettings
from fastapi import FastAPI, Query
from sqlalchemy.sql.expression import func

from wimwb.schemas import UserAgentShort
from wimwb.models import WhatismybrowserUseragent


class Settings(BaseSettings):
    """Application settings"""

    app_name: str = "Whatismywebbrowser database API"
    database_uri: str

    '''
    class Config:  # pylint: disable=too-few-public-methods
        """Automatically load settings from .env file"""

        env_file = ".env"
        env_file_encoding = "utf-8"
    '''


# setup config loading
env = os.environ.get("wimwb_env", "dev")
if env == "test":
    settings = Settings(_env_file=".env.test", _env_file_encoding="utf-8")
else:
    settings = Settings(_env_file=".env", _env_file_encoding="utf-8")

# database related
database = databases.Database(settings.database_uri)
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
async def random_user_agents(limit: int = Query(5, gt=0, le=1000)):
    """Return random user agents"""
    query = (
        user_agents.select()
        .where(user_agents.c.software_type == "browser")
        .order_by(func.rand())
        .limit(limit)
    )
    rows = await database.fetch_all(query=query)
    return rows
