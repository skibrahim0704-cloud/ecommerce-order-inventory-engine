from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from sql.sql_connection import get_db
from sql.sql_models import Order, OrderItem, OrderStatus
from schemas.order_schema import OrderCreate


router = APIRouter(
    prefix="/orders",
    tags=["Orders"]
)


# CREATE ORDER
@router.post("/")
def create_order(
    order_data: OrderCreate,
    db: Session = Depends(get_db)
):
    if not order_data.items:
        raise HTTPException(
            status_code=400,
            detail="Order must contain at least one item"
        )

    # Calculate total amount
    total_amount = 0

    for item in order_data.items:
        total_amount += item.quantity * item.unit_price

    # Create order
    new_order = Order(
        customer_name=order_data.customer_name,
        status=OrderStatus.PENDING,
        total_amount=total_amount
    )

    db.add(new_order)
    db.flush()

    # Create order items
    for item in order_data.items:

        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item.product_id,
            product_name=item.product_name,
            quantity=item.quantity,
            unit_price=item.unit_price
        )

        db.add(order_item)

    db.commit()
    db.refresh(new_order)

    return {
        "message": "Order created successfully",
        "order_id": new_order.id,
        "customer_name": new_order.customer_name,
        "status": new_order.status,
        "total_amount": new_order.total_amount
    }


# GET ALL ORDERS
@router.get("/")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders


# GET ONE ORDER
@router.get("/{order_id}")
def get_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    return order


# UPDATE ORDER STATUS
@router.put("/{order_id}")
def update_order(
    order_id: int,
    status: OrderStatus,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    order.status = status

    db.commit()
    db.refresh(order)

    return {
        "message": "Order updated successfully",
        "order": order
    }


# DELETE ORDER
@router.delete("/{order_id}")
def delete_order(
    order_id: int,
    db: Session = Depends(get_db)
):
    order = (
        db.query(Order)
        .filter(Order.id == order_id)
        .first()
    )

    if not order:
        raise HTTPException(
            status_code=404,
            detail="Order not found"
        )

    db.delete(order)
    db.commit()

    return {
        "message": "Order deleted successfully"
    }
