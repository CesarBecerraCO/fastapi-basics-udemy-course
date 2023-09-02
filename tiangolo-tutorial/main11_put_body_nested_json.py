from typing import Union
from fastapi import FastAPI
from pydantic import BaseModel, HttpUrl

app = FastAPI()

class Image(BaseModel):
    url: HttpUrl #special type, see https://docs.pydantic.dev/latest/usage/types/
    name: str

class Item(BaseModel):
    name: str
    description: Union[str, None] = None
    price: float
    tax: Union[float, None] = None
    tags: set[str] = set() #For unique set of strings
    images: Union[list[Image], None] = None #For list of Umage

class Offer(BaseModel):
    name: str
    description: Union[str, None] = None
    items: list[Item]

@app.put("/offers/")
async def create_offer(offer: Offer):
    return offer

#Nested data example
body_example="""
{
  "name": "hw",
  "description": "hw quotation",
  "items": [
    {
      "name": "firewall",
      "description": "cyber",
      "price": 5000,
      "tax": 1.20,
      "tags": ["fw", "fw", "cyber"],
      "images": [
        {
          "url": "http://127.0.0.1:8000/fw1.jpg",
          "name": "fw1"
        },
        {
          "url": "http://127.0.0.1:8000/fw1.jpg",
          "name": "fw1"
        }
      ]
    },
    {
      "name": "switch",
      "description": "networking",
      "price": 1000,
      "tax": 1.20,
      "tags": ["switch", "networking"]
    }
  ]
}
"""