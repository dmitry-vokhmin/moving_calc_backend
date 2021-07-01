from sqlalchemy.orm import Session
from fastapi import HTTPException
from data_base import models
from schemas import inventory_order as inventory_order_schema


def create(db: Session, inventory_order: inventory_order_schema.InventoryOrderCreate):
    for move_size, value in inventory_order.inventory.items():
        for inventory in value:
            inventory_order_db = models.InventoryOrder(move_size_id=move_size,
                                                       inventory_id=inventory["inventory_id"],
                                                       count=inventory["count"],
                                                       order_id=inventory_order.order_id)
            db.add(inventory_order_db)
    try:
        db.commit()
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=400, detail=str(e))
