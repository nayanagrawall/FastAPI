from typing import List
from fastapi import FastAPI, Depends, status, Response, HTTPException
from . import schemas, models  # as we are importing from same directory therefore used .
from .database import engine, SessionLocal
from sqlalchemy.orm import Session
from .hashing import Hash

app = FastAPI()

models.Base.metadata.create_all(engine)  # to create data in our database


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@app.post('/blog', status_code=status.HTTP_201_CREATED, tags=['Blogs'])
def create(request: schemas.Blog, db: Session = Depends(get_db)):
    new_blog = models.Blog(title=request.title, body=request.body, user_id=1)
    db.add(new_blog)  # Storing the data in our database blog.db
    db.commit()
    db.refresh(new_blog)
    return new_blog


@app.delete('/blog/{id}',
            status_code=status.HTTP_204_NO_CONTENT,
            tags=['Blogs'])  # deleting the data based on the id number in our database
def destroy(id, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    blog.delete(synchronize_session=False)
    db.commit()
    return 'done'


@app.put('/blog/{id}', status_code=status.HTTP_202_ACCEPTED,
         tags=['Blogs'])  # updating the database based on the id number
def update(id, request: schemas.Blog, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id)
    if not blog.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Blog with the id {id} not found")
    blog.update(request.dict())
    db.commit()
    return 'updated successfully'


@app.get('/blog', response_model=List[schemas.ShowBlog],
         tags=['Blogs'])  # to retrieve all the blogs stored in our database
def all(db: Session = Depends(get_db)):
    blogs = db.query(models.Blog).all()
    return blogs


@app.get('/blog/{id}', status_code=200,
         response_model=schemas.ShowBlog, tags=['Blogs'])  # getting the blog from our database based on id number
def show(id, response: Response, db: Session = Depends(get_db)):
    blog = db.query(models.Blog).filter(models.Blog.id == id).first()
    if not blog:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"blog with the id {id} is not available")  # doing the same thing with one single line of code
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'detail': f"blog with the id {id} is not available"}
    return blog


@app.post('/user', response_model=schemas.ShowUser, tags=['Users'])
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash.bcrypt(request.password))  # hashing the password to encrypt it
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@app.get('/user/{id}', response_model=schemas.ShowUser, tags=['Users'])
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")  # doing the same thing with one single line of code
    return user
