from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import BaseModel, Field
from starlette import status

from sqlalchemy.orm import Session
from models import Users #my models.py
from database import SessionLocal #my database.py

from passlib.context import CryptContext  # For hash password

from .auth import get_current_user #This will let us authenticate
user_dependency = Annotated[dict, Depends(get_current_user)] #force authentication and get the token


router = APIRouter(
    prefix='/user',
    tags=['user']
)


#DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]

#READ
@router.get('/', status_code=status.HTTP_200_OK)
async def get_user(user: user_dependency, db: db_dependency):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    return db.query(Users).filter(Users.id == user.get('id')).first()


# For authenticate
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class UserUpdate(BaseModel):
    cur_password: str #to send the current pass
    new_password: str = Field(min_length=6) #after validate cur pass, this will be the new pass

@router.put("/password", status_code=status.HTTP_204_NO_CONTENT)
async def change_password(user: user_dependency, db: db_dependency, user_update: UserUpdate):
    if user is None:
        raise HTTPException(status_code=401, detail='Authentication Failed')
    
    current_user = db.query(Users).filter(Users.id == user.get('id')).first()

    if not bcrypt_context.verify(user_update.cur_password, current_user.hashed_password):
        raise HTTPException(status_code=401, detail='Error on password change')
    
    current_user.hashed_password = bcrypt_context.hash(user_update.new_password)
    db.add(current_user)
    db.commit()
