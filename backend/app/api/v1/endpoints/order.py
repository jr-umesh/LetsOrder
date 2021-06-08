from app.models.order import OrderState
from typing import List, Tuple
from app.models.user import User, UserRole
from app.schemas.order import OrderCreate, OrderInDB, OrderItemCreate, OrderItemInDB, OrderItemRequest
from fastapi import APIRouter, Depends, HTTPException, Body
from sqlalchemy.orm import Session
from app.api.v1.dependencies import CheckRole, get_current_active_user, get_db
from app import crud
from .menu import MENU_ITEM_NOT_FOUND_EXCEPTION

router = APIRouter()


@router.post("/", response_model=OrderInDB, status_code=201)
def place_an_order(
    db: Session = Depends(get_db),
    items: List[OrderItemRequest] = Body(...),
    table_id: int = Body(...),
    current_user: User = Depends(get_current_active_user)
):

    order = crud.order.create(
        db,
        obj_in=OrderCreate(
            table_id=table_id,
            customer_id=current_user.id
        )
    )
    db_items = []
    for item in items:
        if not crud.item.get(db, item.item_id):
            raise MENU_ITEM_NOT_FOUND_EXCEPTION

        db_items.append(crud.order_item.create(
            db,
            obj_in=OrderItemCreate(
                item_id=item.item_id,
                order_id=order.id,
                quantity=item.quantity
            )
        ))
    return crud.order.add_order_items(db, db_obj=order, items=db_items)


@router.get("/queue",
            response_model=List[OrderInDB],
            dependencies=[Depends(CheckRole(UserRole.WAITER))])
def get_order_queue(
    db: Session = Depends(get_db)
):
    """
    gets order which are currently in queue\n
    returned list of orders are sorted by updated date
    """
    return crud.order.get_queue(db)


@router.post("/{order_id}/items", response_model=OrderItemInDB, status_code=201)
def add_order_item(
    order_id: int,
    order_item_in: OrderItemRequest,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    order = crud.order.get(db, order_id)
    if not order:
        raise Exception
    item = crud.item.get(db, order_item_in.item_id)
    if not item:
        raise Exception

    order_item = crud.order_item.create(db, obj_in=OrderItemCreate(
        item_id=order_item_in.item_id,
        order_id=order.id,
        quantity=order_item_in.quantity
    ))

    return crud.order.add_order_item(db, db_obj=order, item=order_item)


@router.delete("/{order_id}/items/{order_item_id}", response_model=OrderItemInDB)
def remove_order_item(
    order_id: int,
    order_item_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    order = crud.order.get(db, order_id)
    if not order:
        raise Exception

    order_item_ids = [o.id for o in order.order_items]
    if order_item_id not in order_item_ids:
        raise Exception

    return crud.order_item.remove(db, id=order_item_id)


@router.put("/{order_id}/cancel", response_model=OrderInDB)
def cancel_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    customer to cancel order
    """
    order = crud.order.get(db, order_id)
    if not order:
        raise Exception

    return crud.order.update_state(db, db_obj=order, state=OrderState.CANCELED)


@router.put("/{order_id}/complete",
            response_model=OrderInDB,
            dependencies=[Depends(CheckRole(UserRole.COOK))])
def complete_order(
    order_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """
    chef when order is complete
    """
    order = crud.order.get(db, order_id)
    if not order:
        raise Exception

    return crud.order.update_state(db, db_obj=order, state=OrderState.COMPLETE)
