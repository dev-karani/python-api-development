from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException
from fastapi.params import Body
from random import randrange
from pydantic import BaseModel
import psycopg
from psycopg.rows import dict_row
import time

app = FastAPI()

#request Get method url "/"
class Post(BaseModel):
    title: str
    content:str
    published: bool = True #optional with default
    rating: Optional[int] = None #optional 

while True:
    try:
        conn =psycopg.connect(
            host='localhost', 
            dbname='fast_api',
            user= 'postgres',
            password='ew',
            row_factory =dict_row
        )

        cursor = conn.cursor() 
        print("Database connection is successful")
        break
    except Exception as Error:
        print("Connection to database failed")
        print("Error: ", Error)
        time.sleep(2)

my_posts = [
    {"title":"title of post 1", "content":"content of post 1", "id":1}, 
    {"title":"favorite foods", "content":"i like pizza", "id":2}
]

@app.get("/")
def root():
    return {"message":"welcome to my final api"}

@app.get("/posts")
def get_posts():
    cursor.execute("""SELECT * FROM posts""")
    posts = cursor.fetchall()
    return {"data": posts}

@app.get("/posts/{id}")
def get_post(id:int):
    cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
    post = cursor.fetchone()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return {"post_detail": post }
 
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
  
@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post:Post):
    cursor.execute("""
        INSERT INTO posts(title, content, published)
        VALUES(%s,%s, %s) RETURNING *
    """, (post.title,post.content, post.publish))
    new_post = cursor.fetchone()
    conn.commit()
    return {"data": new_post}

def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}")
def delete_post(id:int):
    cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    deleted_post = cursor.fetchone()

    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post wit id;{id} does not exist")

    conn.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id:int, post:Post):
        cursor.execute("""
                UPDATE posts
                SET title = %s, content = %s, published = %s
                WHERE id = %s
                RETURNING *
        """, (post.title, post.content, post.published, id))
        updated_post = cursor.fetchone()
        conn.commit()

        if updated_pospt == None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post wit id;{id} does not exist")
     
        return {"data": updated_post}


