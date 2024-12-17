from fastapi import FastAPI

from app.routes.parking_session_router import router as parking_session_router
from app.routes.payment_router import router as payment_router

app = FastAPI()
# TODO: Allow CORS
# TODO: Implement Logging

app.include_router(parking_session_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
