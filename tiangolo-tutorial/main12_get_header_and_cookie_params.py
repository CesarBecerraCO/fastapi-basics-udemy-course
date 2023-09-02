from typing import Annotated, Union
from fastapi import FastAPI, Cookie, Header

app = FastAPI()

@app.get("/items/")
async def read_items(
    ads_id: Annotated[Union[str, None], Cookie()] = None,
    x_tokn: Annotated[Union[str, None], Header()] = None
):
    print(ads_id)
    return {
        "ads_id" : ads_id,
        "X-Token": x_tokn
    }

