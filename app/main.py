from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.routes.parking_session_router import router as parking_session_router
from app.routes.payment_router import router as payment_router

app = FastAPI()
app.add_middleware(CORSMiddleware,
                   allow_origins=['http://localhost:5173'],
                   allow_credentials=True,
                   allow_methods=['*'],
                   allow_headers=['*'])
# TODO: Implement Logging

app.include_router(parking_session_router, prefix="/api/v1")
app.include_router(payment_router, prefix="/api/v1")
