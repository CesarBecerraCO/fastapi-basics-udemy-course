from typing import Annotated, Union
from fastapi import FastAPI, Path, Query

app = FastAPI()

@app.get("/meas/{id}/base/{baseval}")
async def read_items(
    id: Annotated[int, Path(title="Measurand id to get", ge=0, le=100)],
    baseval: Annotated[int, Path(title="Measurand base value", gt=1, le=1000)], #alias gives error :(
    q: Annotated[Union[str, None], Query(alias="meas-name")] = None
):
    results = {"meas-id": id, "base-value": baseval}
    if q:
        results.update({"meas-name": q})
    return results

# http://127.0.0.1:8000/meas/5/base/100?meas-name=voltage

#gt: greater than
#ge: greater than or equal
#lt: less than
#le: less than or equal