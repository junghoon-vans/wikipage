from app import crud
from app import schemas
from app.api.deps import get_db
from fastapi import APIRouter
from fastapi import Depends
from sqlalchemy.orm import Session


router = APIRouter()


@router.get("{post_id}")
def get_post(post_id: int, db: Session = Depends(get_db)):
    return crud.get_post(db, post_id)


@router.get("")
def get_posts(db: Session = Depends(get_db)):
    return crud.get_posts(db)


@router.post("")
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.create_post(db, post)


@router.put("{post_id}")
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db)):
    return crud.update_post(db, post_id, post)


@router.delete("{post_id}")
def delete_post(post_id: int, db: Session = Depends(get_db)):
    return crud.delete_post(db, post_id)
