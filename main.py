from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from routers import inventory, calculate
from routers import user_client
from routers import room_collections
from routers import order
from routers import move_size
from routers import address
from routers import calendar
from routers import floor_collection
from routers import price_tag
from routers import services
from routers import zip_code
from routers import truck
from routers import truck_type
from routers import inventory_collection
from routers import price
from routers import user
from routers import mover_amount
from routers import company
from routers import user_role
from routers import user_privilege
from routers import room
from routers import inventory_category
from routers import inventory_inventory_collection
from routers import inventory_order

app = FastAPI(title="some_service", description="", version="0.0.1")
app.include_router(user.router)
app.include_router(company.router)
app.include_router(inventory.router)
app.include_router(user_client.router)
app.include_router(room_collections.router)
app.include_router(inventory_collection.router)
app.include_router(order.router)
app.include_router(move_size.router)
app.include_router(floor_collection.router)
app.include_router(calendar.router)
app.include_router(price_tag.router)
app.include_router(price.router)
app.include_router(mover_amount.router)
app.include_router(services.router)
app.include_router(address.router)
app.include_router(zip_code.router)
app.include_router(truck.router)
app.include_router(truck_type.router)
app.include_router(calculate.router)
app.include_router(user_role.router)
app.include_router(user_privilege.router)
app.include_router(room.router)
app.include_router(inventory_category.router)
app.include_router(inventory_inventory_collection.router)
app.include_router(inventory_order.router)

app.mount("/images", StaticFiles(directory="images"), name="images")

if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
