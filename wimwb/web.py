import databases
import sqlalchemy
from fastapi import FastAPI
from pydantic import BaseSettings


class Settings(BaseSettings):
    """Application settings"""
    app_name: str = "Whatismywebbrowser database API"
    database_uri: str

    class Config:  # pylint: disable=too-few-public-methods
        """Automatically load settings from .env file"""
        env_file = '.env'
        env_file_encoding = 'utf-8'


# setup things
settings = Settings()
database = databases.Database(settings.database_uri)
metadata = sqlalchemy.MetaData()
engine = sqlalchemy.create_engine(settings.database_uri)

# setup application
app = FastAPI()


@app.on_event("startup")
async def startup():
    await database.connect()


@app.on_event("shutdown")
async def shutdown():
    await database.disconnect()


@app.get("/user_agents/")
async def random_user_agents():
    """Docstring"""
    query = "SELECT * FROM whatismybrowser_useragent LIMIT 5"
    rows = await database.fetch_all(query=query)
    return {"user_agents": rows}
