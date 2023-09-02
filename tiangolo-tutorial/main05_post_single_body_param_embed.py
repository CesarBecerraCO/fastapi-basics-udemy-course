from typing import Union
from fastapi import FastAPI #, Body
from pydantic import BaseModel

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None

app = FastAPI()

@app.post("/items/{itemid}") #POST, to send data you use Request Body
async def create_item(
    itemid: int,
    item: Item, #item: Item = Body(embed=True) #for json_opt_2
    q: Union[str, None] = None
):
    #item_dict = {"item_id": itemid, **item.dict()} #Unpack
    item_dict = item.dict() #Access to item attributes
    item_dict.update({"item_id": itemid})
    if item.tax:
        price_with_tax = item.price + item.tax
        item_dict.update({"price_with_tax": price_with_tax})
    if q:
        item_dict.update({"query_param": q})
    return item_dict
 
#For a single body param
json_opt_1 = """
{
  "name": "firewall",
  "description": "cyber",
  "price": 5000,
  "tax": 1.20
}
"""

#For "embed" a single body param, 
#json opt 2
json_opt_2 = """
{
  "item": {
    "name": "firewall",
    "description": "cyber",
    "price": 5000,
    "tax": 1.20
  }
}
"""