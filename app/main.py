from typing import Optional
from fastapi import FastAPI, Response, status, HTTPException, Depends 
from fastapi.params import Body
from random import randrange
import psycopg
from psycopg.rows import dict_row
import time
import models, schemas
from database import engine, get_db
from sqlalchemy.orm import Session


models.Base.metadata.create_all(bind=engine)

app = FastAPI()


while True:
    try:
        conn =psycopg.connect(
            host='localhost', 
            dbname='fast_api',
            user= 'postgres',
            password='',
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
def get_posts(db: Session = Depends(get_db)):
    posts = db.query(models.Post).all()
    return posts


@app.get("/posts/{id}")
def get_post(id:int, db:Session = Depends(get_db)):
    # cursor.execute(""" SELECT * FROM posts WHERE id = %s""", (id,))
     # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id ==id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id:{id} was not found")
    return post 
 
def find_post(id):
    for p in my_posts:
        if p["id"] == id:
            return p
  

@app.post("/posts", status_code=status.HTTP_201_CREATED)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)):
    new_post = models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


def find_index_post(id):
    for i, p in enumerate(my_posts):
        if p['id'] == id:
            return i

@app.delete("/posts/{id}")
def delete_post(id:int, db:Session = Depends(get_db)):
    # cursor.execute(""" DELETE FROM posts WHERE id = %s RETURNING *""", (id,))
    # deleted_post = cursor.fetchone()
    post = db.query(models.Post).filter(models.Post.id == id)

    if post.first() == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post wit id;{id} does not exist")

    post.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
    
@app.put("/posts/{id}")
def update_post(id:int, post:schemas.PostCreate, db:Session = Depends(get_db)):
        # cursor.execute("""
        #         UPDATE posts
        #         SET title = %s, content = %s, published = %s
        #         WHERE id = %s
        #         RETURNING *
        # """, (post.title, post.content, post.published, id))
        # updated_post = cursor.fetchone()
        # conn.commit()

        post_query = db.query(models.Post).filter(models.Post.id == id)
        existing_post = post_query.first()

        if not existing_post:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post wit id;{id} does not exist")

        post_query.update(post.dict(), synchronize_session=False)
        db.commit()
        return post_query.first()


