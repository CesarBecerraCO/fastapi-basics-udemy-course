from typing import Annotated, Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    email: Annotated[Union[str, None], Query(min_length=3, max_length=50, regex="[\w._%+-]+@[\w.-]+\.[a-zA-Z]{2,4}")] = None
    ):
    results = {"items": [{"item_id": "Foo"}, {"item_id": "Bar"}]}
    if email:
        results.update({"email": email})
    return results