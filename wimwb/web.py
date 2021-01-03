from typing import Optional

from fastapi import FastAPI

app = FastAPI()


@app.get("/")
async def read_root():
    """Docstring"""
    return {"Hello": "World"}


@app.get("/items/{item_id}")
async def read_item(item_id: int, item: Optional[str] = None):
    """Docstring"""
    return {"item_id": item_id, "item": item}
