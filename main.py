from fastapi import FastAPI
from routers import inventory
from routers import user
from routers import room_collections
from routers import order
from routers import move_size
from routers import address
from routers import calendar
from routers import floor_collection
from routers import price_tag
from routers import services
from routers import street
from routers import zip_code
from routers import truck
from routers import truck_type

app = FastAPI(title="some_service", description="", version="0.0.1")
app.include_router(inventory.router)
app.include_router(user.router)
app.include_router(room_collections.router)
app.include_router(order.router)
app.include_router(move_size.router)
app.include_router(address.router)
app.include_router(calendar.router)
app.include_router(floor_collection.router)
app.include_router(price_tag.router)
app.include_router(services.router)
app.include_router(street.router)
app.include_router(zip_code.router)
app.include_router(truck.router)
app.include_router(truck_type.router)


if __name__ == '__main__':
    import uvicorn

    uvicorn.run(app, host="127.0.0.1", port=8080)
