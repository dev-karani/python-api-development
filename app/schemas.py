
from pydantic import BaseModel

#request Get method url "/

class PostBase(BaseModel):
    title: str
    content:str
    published: bool = True #optional with default
    # rating: Optional[int] = None #optional 

class PostCreate(PostBase):
    pass

