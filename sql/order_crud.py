from typing import Optional

from sqlalchemy.orm import Session

from mongodb import product_crud
from sql.sql_models import Order, OrderItem, OrderStatus
from schema.order_schema import OrderCreate, OrderStatusUpdate


class InsufficientStockError(Exception):
    def __init__(self, product_id: str):
        self.product_id = product_id
        super().__init__(f"Insufficient stock for product {product_id}")


class InvalidStatusTransitionError(Exception):
    pass


def create_order(db: Session, products_collection, order_in: OrderCreate) -> Order:
    """
    Places an order across two databases:
      1. Reserve stock atomically in MongoDB for each line item.
      2. Persist the order + items transactionally in MySQL.
    If any reservation fails partway through, everything already
    reserved is rolled back so stock counts never drift.
    """
    reserved: list[tuple[str, int]] = []
    order_items_data = []
    total_amount = 0.0

    try:
        for item in order_in.items:
            product = product_crud.reserve_stock(
                products_collection, item.product_id, item.quantity
            )
            if product is None:
                raise InsufficientStockError(item.product_id)

            reserved.append((item.product_id, item.quantity))
            total_amount += product["price"] * item.quantity
            order_items_data.append(
                OrderItem(
                    product_id=item.product_id,
                    product_name=product["name"],
                    quantity=item.quantity,
                    unit_price=product["price"],
                )
            )
    except InsufficientStockError:
        for product_id, quantity in reserved:
            product_crud.release_stock(products_collection, product_id, quantity)
        raise

    order = Order(
        customer_name=order_in.customer_name,
        status=OrderStatus.PENDING,
        total_amount=total_amount,
        items=order_items_data,
    )
    db.add(order)
    db.commit()
    db.refresh(order)
    return order


def get_order(db: Session, order_id: int) -> Optional[Order]:
    return db.query(Order).filter(Order.id == order_id).first()


def list_orders(db: Session) -> list[Order]:
    return db.query(Order).all()


_ALLOWED_TRANSITIONS = {
    OrderStatus.PENDING: {OrderStatus.CONFIRMED, OrderStatus.CANCELLED},
    OrderStatus.CONFIRMED: {OrderStatus.SHIPPED, OrderStatus.CANCELLED},
    OrderStatus.SHIPPED: {OrderStatus.DELIVERED},
    OrderStatus.DELIVERED: set(),
    OrderStatus.CANCELLED: set(),
}


def update_order_status(
    db: Session, products_collection, order_id: int, update: OrderStatusUpdate
) -> Optional[Order]:
    order = get_order(db, order_id)
    if order is None:
        return None

    if update.status not in _ALLOWED_TRANSITIONS[order.status]:
        raise InvalidStatusTransitionError(
            f"Cannot move order from {order.status} to {update.status}"
        )

    if update.status == OrderStatus.CANCELLED:
        for item in order.items:
            product_crud.release_stock(products_collection, item.product_id, item.quantity)

    order.status = update.status
    db.commit()
    db.refresh(order)
    return order

