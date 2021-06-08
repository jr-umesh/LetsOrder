from app.models.user import UserRole
from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

from app.schemas import UserInDB, UserCreate, UserUpdate
from app.models import Image, User
from app.api.v1.dependencies import get_db, upload_image, get_current_active_user, CheckRole
from app import crud

router = APIRouter()


@router.post("/register", response_model=UserInDB, status_code=201)
def register_user(
    *,
    db: Session = Depends(get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Register by a new user
    """
    user = crud.user.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = UserCreate(
        password=password, email=email, full_name=full_name)
    user = crud.user.create(db, obj_in=user_in)
    return user


@router.post("/me/profile-pic")
def add_profile_pic(*,
                    image: Image = Depends(upload_image),
                    db: Session = Depends(get_db),
                    current_user: User = Depends(get_current_active_user)):
    """
    add a new profile picture for the user
    """
    user = crud.user.get(db, id=current_user.id)
    crud.user.add_profile_pic(db, db_obj=user, image=image)
    return {"url": image.url}


@router.get("/me", response_model=UserInDB)
def read_user_me(
    current_user: User = Depends(get_current_active_user)
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=UserInDB)
def update_user_me(
    *,
    db: Session = Depends(get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: User = Depends(
        get_current_active_user),
) -> Any:
    """
    Update own user.
    """
    current_user_data = jsonable_encoder(current_user)
    user_in = UserUpdate(**current_user_data)
    if password is not None:
        user_in.password = password
    if full_name is not None:
        user_in.full_name = full_name
    if email is not None:
        user_in.email = email
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{usr_id}",
            response_model=UserInDB,
            dependencies=[Depends(CheckRole(UserRole.MANAGER))])
def get_user(
    usr_id: int,
    db: Session = Depends(get_db),
):
    user = crud.user.get(db, id=usr_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    return user


@router.get("/",
            response_model=List[UserInDB],
            dependencies=[Depends(CheckRole(UserRole.MANAGER))])
def read_users(
    db: Session = Depends(get_db),
    skip: int = 0,
    limit: int = 100,
) -> Any:
    """
    Retrieve users.
    """
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users
