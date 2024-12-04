from fastapi import FastAPI
from app.routes.transaction_router import router as transaction_router
from app.routes.vehicle_router import router as vehicle_router
from app.routes.extra_router import router as extra_router

app = FastAPI()
# TODO: Implement CORS
# TODO: Implement Logging

# TODO: Implement DRY principle here
app.include_router(transaction_router, prefix="/api/v1")
app.include_router(vehicle_router, prefix="/api/v1")
app.include_router(extra_router, prefix="/api/v1")
