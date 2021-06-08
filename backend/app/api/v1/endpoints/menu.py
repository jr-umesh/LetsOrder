from app.schemas.item import ItemUpdate
from app.models.image import Image
from app.models.user import UserRole
from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.api.v1.dependencies import CheckRole, get_db, upload_image
from app import crud
from app.schemas import ItemInDB, ItemCreate

router = APIRouter()

MENU_ITEM_NOT_FOUND_EXCEPTION = HTTPException(
    status_code=404, detail="menu item not found!")


@router.get("/", response_model=List[ItemInDB])
def get_menu(
    db: Session = Depends(get_db)
):
    return crud.item.get_menu(db)


@router.post("/",
             response_model=ItemInDB,
             dependencies=[Depends(CheckRole(UserRole.MANAGER))],
             status_code=201)
def create_menu_item(
    menu_item_in: ItemCreate,
    db: Session = Depends(get_db),
):
    return crud.item.create(db, obj_in=menu_item_in)


@router.get("/{item_id}",
            response_model=ItemInDB)
def get_menu_item(
    item_id: int,
    db: Session = Depends(get_db)
):
    menu_item = crud.item.get(db, item_id)
    if not menu_item:
        raise MENU_ITEM_NOT_FOUND_EXCEPTION
    return menu_item


@router.put("/{item_id}",
            response_model=ItemInDB,
            dependencies=[Depends(CheckRole(UserRole.MANAGER))])
def update_menu_item(
    item_id: int,
    menu_item_in: ItemUpdate,
    db: Session = Depends(get_db)
):
    menu_item = crud.item.get(db, item_id)
    if not menu_item:
        raise MENU_ITEM_NOT_FOUND_EXCEPTION
    return crud.item.update(db, db_obj=menu_item, obj_in=menu_item_in)


@router.delete("/{item_id}",
               response_model=ItemInDB,
               dependencies=[Depends(CheckRole(UserRole.MANAGER))])
def remove_item_from_menu(item_id: int, db: Session = Depends(get_db)):
    menu_item = crud.item.get(db, item_id)
    if not menu_item:
        raise MENU_ITEM_NOT_FOUND_EXCEPTION
    return crud.item.remove_from_menu(db, db_obj=menu_item)


@router.put("/{item_id}/image",
            response_model=ItemInDB,
            dependencies=[Depends(CheckRole(UserRole.MANAGER))])
def change_item_image(
    item_id: int,
    db: Session = Depends(get_db),
    image: Image = Depends(upload_image)
):
    menu_item = crud.item.get(db, item_id)
    if not menu_item:
        raise MENU_ITEM_NOT_FOUND_EXCEPTION
    return crud.item.change_image(db, menu_item, image)
