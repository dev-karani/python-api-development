
from pydantic import BaseModel, EmailStr
from datetime import datetime
#request Get method url "/

class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True #optional with default
    # rating: Optional[int] = None #optional 

class PostCreate(PostBase):
    pass

class Post(PostBase):
    id:int 
    created_at:datetime

    class Config:
        orm_mode =True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime

    class Config:
        orm_mode =True