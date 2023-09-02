from fastapi import FastAPI
import models #my models.py
from database import engine #my database.py
from routers import todos, auth, admin, users #my routers/...

app = FastAPI()

#From models.py and database.py, create all defined tables
#this will be ran only if todosapp.db does not exist 
models.Base.metadata.create_all(bind=engine)


#Include routers
app.include_router(auth.router)
app.include_router(todos.router)
app.include_router(admin.router)
app.include_router(users.router)
