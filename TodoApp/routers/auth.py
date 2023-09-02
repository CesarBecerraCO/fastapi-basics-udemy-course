from datetime import datetime, timedelta

from typing import Annotated
from fastapi import APIRouter, Depends, Path, HTTPException
from pydantic import BaseModel
from starlette import status

from sqlalchemy.orm import Session
from models import Users  # my models.py
from database import SessionLocal  # my database.py

from fastapi.security import OAuth2PasswordRequestForm, OAuth2PasswordBearer # For authenticate user
from passlib.context import CryptContext  # For hash password
from jose import jwt, JWTError  # For JWT


router = APIRouter(
    prefix="/auth", tags=["auth"]
)

#DB Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

db_dependency = Annotated[Session, Depends(get_db)]



# For authenticate
bcrypt_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
# For authenticate user
def authenticate_user(username: str, password: str, db):
    user = db.query(Users).filter(Users.username == username).first()
    if not user:
        return False
    if not bcrypt_context.verify(password, user.hashed_password):
        return False
    return user



# For creating token
SECRET_KEY = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXxx"
ALGORITHM = "XSXAXAS"
# For creating access token
def create_access_token(username: str, user_id: int, role: str, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id, "role": role}
    expires = datetime.utcnow() + expires_delta
    encode.update({"exp": expires})
    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)



# Pydantic class
class Token(BaseModel):
    access_token: str
    token_type: str

# ENCODING: Authenticate and Create a JWT object
@router.post("/token", response_model=Token) #response is the Token!!!
async def login_for_access_token(db: db_dependency, form_data: Annotated[OAuth2PasswordRequestForm, Depends()]):
    #Authenticate
    user = authenticate_user(form_data.username, form_data.password, db)
    if not user:
        # return {'auth': 'Failed'}
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )
    # ENCODING, get access token
    token = create_access_token(user.username, user.id, user.role, timedelta(minutes=20))
    return {"access_token": token, "token_type": "bearer"}




# For DECODING dependency
# "auth/token" calls login_for_access_token()
oauth2_bearer = OAuth2PasswordBearer(tokenUrl="auth/token")
# For DECODING, not an endpoint, later we will use it
async def get_current_user(token: Annotated[str, Depends(oauth2_bearer)]):
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM]) #DECODING!!!
        username: str = payload.get("sub")
        user_id: int = payload.get("id")
        user_role: int = payload.get("role")
        if username is None or user_id is None:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Could not validate user.",
            )
        return {"username": username, "id": user_id, "user_role": user_role} #Ok, returns only username and id
    except JWTError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate user."
        )





# READ, this is just a test
@router.get("/", status_code=status.HTTP_200_OK)
async def get_cesar_test():
    return {"user": "Cesar"}


# READ
@router.get("/users", status_code=status.HTTP_200_OK)
async def get_users(db: db_dependency):
    return db.query(Users).all()  # query all records by using Todos model, nice!


# Pydantic class
class UserRequest(BaseModel):
    username: str
    email: str
    first_name: str
    last_name: str
    password: str
    role: str

    # This is for see an schema example on /docs
    model_config = {
        "json_schema_extra": {
            "example": {
                "username": "cesbecer",
                "email": "cesbecer@gmail.com",
                "first_name": "Cesar",
                "last_name": "Becerra",
                "password": "a9a209m3xjuq39",
                "role": "admin",
            }
        }
    }


# CREATE
@router.post("/", status_code=status.HTTP_201_CREATED)
async def create_user(db: db_dependency, user_request: UserRequest):
    new_user = Users(
        email=user_request.email,
        username=user_request.username,
        first_name=user_request.first_name,
        last_name=user_request.last_name,
        role=user_request.role,
        hashed_password=bcrypt_context.hash(user_request.password),
        is_active=True,
    )

    db.add(new_user)
    db.commit()


# DELETE
@router.delete("/user/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(db: db_dependency, user_id: int = Path(gt=0)):
    user_obj = db.query(Users).filter(Users.id == user_id).first()
    if user_obj is None:
        raise HTTPException(status_code=404, detail="User not found.")

    db.query(Users).filter(Users.id == user_id).delete()
    db.commit()
