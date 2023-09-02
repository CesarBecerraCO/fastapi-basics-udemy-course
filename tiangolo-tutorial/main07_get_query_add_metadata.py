#from typing import List       #for Python < v3.9, to use List[str]
from typing import Annotated, Union
from fastapi import FastAPI, Query

app = FastAPI()

@app.get("/items/")
async def read_items(
    e: Annotated[Union[list[str], None], Query(
        title="Lista de elementos",
        description="Elementos asociados a sistemas eléctricos de potencia",
        min_length=3, # min string length. En Swagger UI (.../docs) también usa ese valor como la cantidad min de elementos de la lista (Bug?)
        alias="electrical-elements", #en la url, en vez de pasar e, pasas electrical-elements
        deprecated=False, #True cuando quieras advertir que no sigan pasando este dato (solo es una nota)
        include_in_schema=True #False si quieres ocultar el parámetro
    )] = ["trafos", "generadores"] # For default values
):
    query_list_items = {"lista": e}
    return query_list_items

#http://127.0.0.1:8000/items/?electrical-elements=trafos&electrical-elements=generadores&electrical-elements=barras

#Use list with not type def, but no validations is made:
#async def read_items(e: Annotated[Union[list, None], Query()] = []):