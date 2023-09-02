from enum import Enum
from typing import Union
from fastapi import FastAPI

class Measurand(str, Enum):
    voltage = "voltage"
    current = "current"
    active_power = "acpower"
    reactive_power = "repower"
    frequency = "freq"

app = FastAPI()

@app.get("/lamp/{lampid}")
async def get_lamp_status(lampid: int, name: Union[str, None] = None, poweron: bool = False):
    lamp = {"lamp_id": lampid, "power_on": poweron}
    if name:
        lamp.update({"lamp_name": name})
    if poweron:
        lamp.update(
            {"warning": "This amazing lamp is consuming energy"}
        )
    return lamp 

@app.get("/measurand/{meas}") #meas is a PATH parameter, from list
async def get_meas(meas: Measurand, base: float = 100, cur_value: float = 100): #base and cur_value are QUERY parameters 
    return {"meas_key": meas, "meas_name": meas.name,
            "base_value": base, "current_value": cur_value, 
            "pu": cur_value/base}

@app.get("/")
async def root():
    return {"message": "Measurand calculation"}

# uvicorn main:app --reload