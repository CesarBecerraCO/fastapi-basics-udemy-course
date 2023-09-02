from enum import Enum
from fastapi import FastAPI

class Measurand(str, Enum):
    voltage = "voltage"
    current = "current"
    active_power = "acpower"
    reactive_power = "repower"
    frequency = "freq"

app = FastAPI()

@app.get("/measurand/{meas}") #meas is a PATH parameter, from list
async def get_meas(meas: Measurand, base: float, cur_value: float): #base and cur_value are QUERY parameters 
    return {"meas_key": meas, "meas_name": meas.name,
            "base_value": base, "current_value": cur_value, 
            "pu": cur_value/base}

@app.get("/")
async def root():
    return {"message": "Measurand calculation"}

# uvicorn main:app --reload