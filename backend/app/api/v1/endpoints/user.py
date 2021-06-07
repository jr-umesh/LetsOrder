from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from pydantic.networks import EmailStr
from sqlalchemy.orm import Session

router = APIRouter()


@router.post("/register", response_model=User)
def register_user(
    *,
    image: Image = Depends(upload_image),
    db: Session = Depends(database.get_db),
    password: str = Body(...),
    email: EmailStr = Body(...),
    full_name: str = Body(None),
) -> Any:
    """
    Create new user.
    """
    user = user_repo.get_by_email(db, email=email)
    if user:
        raise HTTPException(
            status_code=400,
            detail="The user with this username already exists in the system",
        )
    user_in = UserCreate(
        password=password, email=email, full_name=full_name)
    user = user_repo.create(db, obj_in=user_in)
    user_repo.add_profile_pic(db, db_obj=user, image=image)
    return user


@router.post("/me/profile-pic")
def add_profile_pic(*,
                    image: Image = Depends(upload_image),
                    db: Session = Depends(database.get_db),
                    current_user: User = Depends(auth.get_current_active_user)):
    user = user_repo.get(db, id=current_user.id)
    user_repo.add_profile_pic(db, db_obj=user, image=image)
    return {"url": image.url}


@router.get("/me", response_model=User)
def read_user_me(
    db: Session = Depends(database.get_db),
    current_user: User = Depends(
        auth.get_current_active_user),
) -> Any:
    """
    Get current user.
    """
    return current_user


@router.put("/me", response_model=User)
def update_user_me(
    *,
    db: Session = Depends(database.get_db),
    password: str = Body(None),
    full_name: str = Body(None),
    email: EmailStr = Body(None),
    current_user: User = Depends(
        auth.get_current_active_user),
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
    user = user_repo.update(db, db_obj=current_user, obj_in=user_in)
    return user


@router.get("/{usr_id}", response_model=User)
def get_user(
    usr_id: int,
    db: Session = Depends(database.get_db)
):
    user = user_repo.get(db, id=usr_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="user not found"
        )
    return user


@router.get("/", response_model=List[User])
def read_users(
    db: Session = Depends(database.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(
        auth.get_current_active_user),
) -> Any:
    """
    Retrieve users.
    """
    users = user_repo.get_multi(db, skip=skip, limit=limit)
    return users
