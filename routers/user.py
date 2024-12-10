from fastapi import APIRouter, Depends, status, HTTPException
from sqlalchemy.orm import Session
from app.backend.db_depends import get_db
from typing_extensions import Annotated, Any
from app.models import User
from app.schemas import CreateUser, UpdateUser
import sqlalchemy
from sqlalchemy import insert, select, update, delete
from slugify import slugify

router = APIRouter(prefix='/user', tags=['user'])


@router.get("/")
async def all_users(db: Annotated[Session, Depends(get_db)]):
    users = db.scalar(select(User))
    return users


@router.get("/user_id")
async def user_by_id(db: Annotated[Session, Depends(get_db)], user_id):
    user_ident = db.scalar(select(User).where(User.id == user_id))
    if user_ident is not None:
        return user_ident
    raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                        detail="User was not found")


@router.post("/create")
async def create_user(db: Annotated[Session, Depends(get_db)], create_user: CreateUser):
    db.execute(insert(User).values(username=create_user.username,
                                   firstname=create_user.firstname,
                                   lastname=create_user.lastname,
                                   age=create_user.age,
                                   slug=slugify(create_user.username)))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': "Successful"}


@router.put("/update")
async def update_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: Any):
    user_ident = db.scalar(select(User).where(User.id == user_id))
    if user_ident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    db.execute(UpdateUser().where(User.id == user_id).update(
        firstname=update_user.firstname,
        lastname=update_user.lastname,
        age=update_user.age))
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': "Successful"}


@router.delete("/delete")
async def delete_user(db: Annotated[Session, Depends(get_db)], update_user: UpdateUser, user_id: Any):
    user_ident = db.scalar(select(User).where(User.id == user_id))
    if user_ident is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail="User was not found")
    db.execute(UpdateUser().where(User.id == user_id).delete())
    db.commit()
    return {'status_code': status.HTTP_201_CREATED,
            'transaction': "Successful"}
