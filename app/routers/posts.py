from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session
from .. import models, schemas, utils,auth2
from ..database import get_db
from typing import Optional, List
from sqlalchemy import func
router= APIRouter(prefix = "/posts",
                  tags= ['Posts'])


#@router.get("/", response_model = List[schemas.Post])
@router.get("/", response_model = List[schemas.Post_Out])
#@router.get("/")
def get_posts(db:Session= Depends(get_db), current_user: int= Depends(auth2.get_current_user),limit: int= 10, skip:int= 0, search: Optional[str]= ""):
    #cursor.execute("""SELECT * FROM posts""")
    #posts = cursor.fetchall()
    #print(limit)
    all_posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter= True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #print(results)
    return results

@router.post("/", status_code = status.HTTP_201_CREATED, response_model = schemas.Post)
def create_posts(post: schemas.PostCreate, db:Session = Depends(get_db), current_user: int= Depends(auth2.get_current_user)):
    #cursor.execute(""" INSERT INTO posts (title, content, published) VALUES (%s, %s, %s) RETURNING * """, (post.title, post.message, post.published))
    #new_post = cursor.fetchone()
    #conn.commit()
    
    new_post = models.Post(user_id= current_user.id, title = post.title, content = post.content, published = post.published)
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}", response_model = schemas.Post)
def get_post(id : int, db: Session= Depends(get_db), current_user:int=Depends(auth2.get_current_user)):
    #cursor.execute("""SELECT * FROM posts WHERE id = %s""", (str(id),))
    #get_post = cursor.fetchone()
    get_post = db.query(models.Post).filter(models.Post.id == id).first()
    getting_one = db.query(models.Post, func.count(models.Vote.post_id).label('votes'), isouter= True).join(models.Vote, models.Vote.post_id == models.Post.id).group_by(models.Post.id).filter(models.Post.id == id).first()
    if not getting_one:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = f"post with id of: {id} was not found")
    
    return  getting_one 

@router.delete("/posts/{id}", status_code = status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session= Depends(get_db), current_user: int= Depends(auth2.get_current_user)):
    post_check = db.query(models.Post).filter(models.Post.id == id)
    #cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, (str(id),))
    #delete_post = cursor.fetchone()
    #conn.commit()
    post = post_check.first()
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "post with such id does not exist, sorry...")
    
    if post.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized..sorry.")
    post.delete(synchronize_session = False)
    db.commit()
    return Response(status_code = status.HTTP_204_NO_CONTENT)

@router.put("/{id}", response_model = schemas.Post)
def update_post(id: int, post: schemas.PostCreate, db:Session= Depends(get_db), current_user:int=Depends(auth2.get_current_user)):
    #cursor.execute("""UPDATE posts SET title = %s, content = %s, published = %s WHERE id = %s""", (post.title, post.message, post.published, str(id)),)
    #updated_post = cursor.fetchone()
    #conn.commit()
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post2 = post_query.first()
    if post2 == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND, detail = "post with the listed index was not found")
    
    if post2.user_id != current_user.id:
        raise HTTPException(status_code= status.HTTP_403_FORBIDDEN, detail= "Not authorized..sorry")
    post_query.update(post2.dict(), synchronize_session = False)
    db.commit()

    return post_query.first()