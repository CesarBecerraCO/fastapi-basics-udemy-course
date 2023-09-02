from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}

# From console:
# dev\py\fastapi>uvicorn main:app --reload