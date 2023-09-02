from typing import Annotated, Union
from fastapi import Body, Path, FastAPI
from pydantic import BaseModel, Field #Field for validation and metadata inside of Pydantic models 

app = FastAPI()

#Pydantic model
class Item(BaseModel):
    name: str
    description: Union[str, None] = Field( #for validation and metadata
        default=None, 
        title="The description of the item", 
        min_length=10,
        max_length=23
    )
    price: float = Field( #for validation and metadata
        gt=0, 
        description="The price must be greater than zero"
    )
    tax: Union[float, None] = None

@app.put("/items/{item_id}")
async def update_item(
    item_id: Annotated[int, Path(title="Id to get", ge=1, le=100)], #Path parameter validation and metadata
    item: Annotated[Item, Body(embed=True)] #See Item for validation and metadata
):
    results = {"item_id": item_id, "item": item}
    return results
