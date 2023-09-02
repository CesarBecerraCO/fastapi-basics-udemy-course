from typing import Annotated, Union
from fastapi import FastAPI, Path, Body
from pydantic import BaseModel

app = FastAPI()

#Body param
class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

#Body param
class User(BaseModel):
    username: str
    full_name: Union[str, None] = None

#Body param for "level"? No!, just make a singular definition, not a class


@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="The ID of the item to get", ge=0, le=1000)], #path param is mandatory
    level: Annotated[int, Body(gt=0)], #mandatory "singular" body param 
    q: Union[str, None] = None, #optional query param, because the default setting to None
    item: Union[Item, None] = None, #optional body param
    user: Union[User, None] = None, #optional body param
):
    results = {"item_id": item_id, "level": level}
    if q:
        results.update({"q": q})
    if item:
        results.update({"item": item})
    if user:
        results.update({"user": user})
    return results

#request body example
rb = """
{
  "level": 10,
  "item": {
    "name": "firewall",
    "description": "cybersecurity",
    "price": 5000,
    "tax": 2.20
  },
  "user": {
    "username": "cesbecer",
    "full_name": "César Becerra"
  }
}
"""