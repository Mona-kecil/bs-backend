from fastapi import FastAPI

from app.routes.parking_session_router import router as parking_session_router

app = FastAPI()
# TODO: Implement CORS
# TODO: Implement Logging

app.include_router(parking_session_router, prefix="/api/v1")
