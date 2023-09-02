from fastapi import FastAPI

myApp = FastAPI()

@myApp.get("/")
async def root():
    return {"message": "Hello World"}

# From console:
# dev\py\fastapi>uvicorn main0:myApp --reload