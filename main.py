from typing import Optional
from fastapi import FastAPI
from fastapi.params import Body
from pydantic import BaseModel

app = FastAPI()

#request Get method url "/"
class Post(BaseModel):
    title: str
    content:str
    publish: bool = True #optional with default
    rating: Optional[int] = None #optional 

@app.get("/")
def root():
    return {"message":"welcome to my final api"}

@app.get("/posts")
def get_posts():
    return {"data":"this is your posts"}
  
@app.post("/createposts")
def createposts(post:Post):
    print(post)
    print(post.dict())
    return {"data": post}
