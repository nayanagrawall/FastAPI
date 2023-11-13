from fastapi import APIRouter, Depends, HTTPException, status
from .. import schemas, database, models
from ..hashing import Hash
from sqlalchemy.orm import Session

router = APIRouter(
    prefix="/user",
    tags=['Users']
)
get_db = database.get_db


@router.post('/', response_model=schemas.ShowUser)
def create_user(request: schemas.User, db: Session = Depends(get_db)):
    new_user = models.User(name=request.name, email=request.email,
                           password=Hash.bcrypt(request.password))  # hashing the password to encrypt it
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


@router.get('/{id}', response_model=schemas.ShowUser)
def get_user(id: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {id} is not found")  # doing the same thing with one single line of code
    return user
