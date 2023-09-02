from enum import Enum
from fastapi import FastAPI

class ModelName(str, Enum):
    station = "station"
    subnet = "subnet"
    bay = "bay"

app = FastAPI()

@app.get("/models/{model_name}") #parameter from list
async def get_model(model_name: ModelName):
    if model_name is ModelName.station: return {"model_name": model_name, "type": "Station!"}
    if model_name.value == "level": return {"model_name": model_name, "type": "For voltage Level!"}
    return {"model_name": model_name, "type": "Is a bay"}

@app.get("/users/me")
async def read_user_me(): #No parameter
    return {"user_id": "the current user"}

@app.get("/items/{item_id}") #parameter to pass in url
async def read_item(item_id: int):
    return {"item_id": item_id}

@app.get("/")
async def root():
    return {"message": "Hello Cesar!"}

# uvicorn main:app --reload