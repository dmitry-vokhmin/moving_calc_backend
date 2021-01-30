from fastapi import FastAPI
from routers import inventory
from routers import user
from routers import room_collections
from routers import order
from routers import move_size

app = FastAPI(title="some_service", description="", version="0.0.1")
app.include_router(inventory.router)
app.include_router(user.router)
app.include_router(room_collections.router)
app.include_router(order.router)
app.include_router(move_size.router)

if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8080)
