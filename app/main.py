from fastapi import FastAPI
from blog import models  # as we are importing from same directory therefore used .
from blog.database import engine
from blog.routers import blog, user, authentication

app = FastAPI()

models.Base.metadata.create_all(engine)  # to create data in our database

app.include_router(authentication.router)
app.include_router(blog.router)
app.include_router(user.router)

# def get_db():
#     db = SessionLocal()
#     try:
#         yield db
#     finally:
#         db.close()


# @app.get('/blog', response_model=List[schemas.ShowBlog],
#          tags=['Blogs'])  # to retrieve all the blogs stored in our database
# def all(db: Session = Depends(get_db)):
#     blogs = db.query(models.Blog).all()
#     return blogs

# https://youtu.be/7t2alSnE2-I?feature=shared&t=11716
