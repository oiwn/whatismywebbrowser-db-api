import os
from typing import List
from datetime import datetime, timedelta

import databases
import sqlalchemy
from pydantic import BaseSettings
from fastapi import FastAPI, Query
from sqlalchemy.sql import and_
from sqlalchemy.sql.expression import func

from wimwb.schemas import UserAgentShort
from wimwb.models import WhatismybrowserUseragentModel


class Settings(BaseSettings):
    """Application settings"""

    app_name: str = "Whatismywebbrowser database API"
    database_uri: str


# setup config loading
env = os.environ.get("WIMWB_ENV", "dev")

# TODO: this is total mess, need to find a way to
# split settings to 3 env - docker, dev and test
if os.path.exists(".env"):
    settings = Settings(_env_file=".env", _env_file_encoding="utf-8")
    if env == "test":
        settings = Settings(_env_file=".env.test", _env_file_encoding="utf-8")

# database related
database = databases.Database(settings.database_uri)
engine = sqlalchemy.create_engine(settings.database_uri)
user_agents = WhatismybrowserUseragentModel.__table__  # pylint: disable=E1101


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
async def random_user_agents(
    software_type: str = "browser",
    limit: int = Query(5, gt=0, le=1000),
    seen_times_gt: int = Query(1000, gt=0),
    updated_back_weeks: int = Query(100, gt=0),
):
    """Return random user agents"""
    how_old = datetime.utcnow() - timedelta(weeks=updated_back_weeks)

    query = (
        user_agents.select()
        .where(
            and_(
                user_agents.c.software_type == software_type,
                user_agents.c.times_seen >= seen_times_gt,
                user_agents.c.last_seen_at >= how_old,
            )
        )
        .order_by(func.random())
        .limit(limit)
    )
    rows = await database.fetch_all(query=query)
    return rows
