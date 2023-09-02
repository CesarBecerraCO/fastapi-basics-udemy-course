from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status

from sqlalchemy.orm import Session
from models import Todos #my models.py
from database import SessionLocal #my database.py


from .auth import get_current_user #This will let us authenticate
user_dependency = Annotated[dict, Depends(get_current_user)] #force authentication and get the token


router = APIRouter( #Notice this for router
    tags=['todo']
) 


#DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
#Annotated define db_dependency as type "Session" (from sqlalchemy.orm)
#and Depends is for doing something before to execute something else (dependency inyection)
db_dependency = Annotated[Session, Depends(get_db)]



#READ
@router.get("/", status_code=status.HTTP_200_OK)
async def read_all_todos(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    #query all todos, filtered by user X, by using Todos model, nice!
    return db.query(Todos).filter(Todos.owner_id == user.get('id')).all() 

#READ
@router.get("/todo/{todo_id}", status_code=status.HTTP_200_OK)
async def read_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    todo_obj = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_obj is not None:
        return todo_obj
    raise HTTPException(status_code=404, detail='Todo not found.')


#Pydantic class
class TodoRequest(BaseModel):
    #id is not passed, see the model
    title: str = Field(min_length=3)
    description: str = Field(min_length=3, max_length=100)
    priority: int = Field(gt=0, lt=6)
    complete: bool
    #role_id is not passed

    #This is for see an schema example on /docs
    model_config = {
        "json_schema_extra" : {
            'example': {
                'title': 'A new todo title',
                'description': 'do something',
                'priority': 5,
                'complete': False,
            }
        }
    }


#CREATE
#Using Auth and Token
@router.post("/todo", status_code=status.HTTP_201_CREATED)
async def create_todo(user: user_dependency, db: db_dependency, todo_request: TodoRequest):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")

    new_todo = Todos(**todo_request.model_dump(), owner_id=user.get('id'))
    db.add(new_todo)
    db.commit()


#UPDATE
@router.put("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def update_todo(user:user_dependency, db: db_dependency, todo_request: TodoRequest, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    todo_obj = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_obj is None:
        raise HTTPException(status_code=404, detail='Todo not found.')

    todo_obj.title = todo_request.title
    todo_obj.description = todo_request.description
    todo_obj.priority = todo_request.priority
    todo_obj.complete = todo_request.complete

    db.add(todo_obj)
    db.commit()


#DELETE
@router.delete("/todo/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_todo(user:user_dependency, db: db_dependency, todo_id: int = Path(gt=0)):
    if user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Authentication failed")
    
    todo_obj = db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).first()
    if todo_obj is None:
        raise HTTPException(status_code=404, detail='Todo not found.')
    
    db.query(Todos).filter(Todos.id == todo_id).filter(Todos.owner_id == user.get('id')).delete()
    db.commit()