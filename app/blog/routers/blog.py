from typing import List
from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session
from ..oauth2 import get_current_user
from .. import schemas, database, models
from ..repository import blog

router = APIRouter(
    prefix="/blog",
    tags=['Blogs']  # Providing custom tag for this router
)
get_db = database.get_db


@router.get('/', response_model=List[schemas.ShowBlog])  # to retrieve all the blogs stored in our database
def all(db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.get_all(
        db)  # We are fetching the database from repository folder which is having blog.py file and code for fetching is written over there


@router.post('/', status_code=status.HTTP_201_CREATED)
def create(request: schemas.Blog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    return blog.create(request,
                       db)  # Fetching the required database from repository folder which is having a blog.py file and code is written in it.


@router.delete('/{id}',
               status_code=status.HTTP_204_NO_CONTENT)  # deleting the data based on the id number in our database
def destroy(id, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.delete(id, db)


@router.put('/{id}', status_code=status.HTTP_202_ACCEPTED)  # updating the database based on the id number
def update(id, request: schemas.Blog, db: Session = Depends(get_db),
           current_user: schemas.User = Depends(get_current_user)):
    return blog.update(id, request, db)


@router.get('/{id}', status_code=200,
            response_model=schemas.ShowBlog)  # getting the blog from our database based on id number
def show(id, response: Response, db: Session = Depends(get_db), current_user: schemas.User = Depends(get_current_user)):
    return blog.show(id, db)
