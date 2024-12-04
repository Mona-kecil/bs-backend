from fastapi import APIRouter, Query, Path
from typing import Annotated
from pydantic import BaseModel
from enum import Enum
from datetime import datetime
from app.services import supabase_service

router = APIRouter()


class PaymentStatus(str, Enum):
    unpaid = 'Unpaid'
    paid = 'Paid'
    manual = 'Manual'


class PaymentMethod(str, Enum):
    mobile = 'Mobile'
    kiosk = 'Kiosk'
    manual = 'Manual'


class TransactionPost(BaseModel):
    license_plate: str
    entry_time: datetime
    payment_status: PaymentStatus


class TransactionPatch(TransactionPost):
    exit_time: datetime
    fee: int
    payment_status: PaymentStatus
    payment_method: PaymentMethod
    payment_time: datetime
    payment_expiry_time: datetime


@router.get("/transactions")
async def get_transactions(
        skip: Annotated[int | None, Query(title="Offset", gt=0)] = None,
        limit: Annotated[int | None, Query(title="Limit", gt=0, le=100)] = None
):
    """
    Fetch all transactions from the database

    @param skip: Offset
    @param limit: Limit

    @return: All transactions from offset to limit
    """
    # TODO: Implement pagination
    response = supabase_service.get_transactions()
    return response.data


@router.get("/transactions/{id}")
async def get_transaction_by_id(
    id: Annotated[int | None, Path(title="Transaction ID", gt=0)]
):
    """
    Fetch specific transaction by ID

    @param id: Transaction ID

    @return: Transaction with given ID
    """
    response = supabase_service.get_transaction_by_id(id)
    return response.data


@router.post("/transactions")
async def create_transaction(
    data: Annotated[dict, TransactionPost]
):
    """
    Create a new transaction to the database

    @param data: Transaction data

    @return: Newly created transaction
    """
    response = supabase_service.insert_data("transactions", data)
    return response.data


@router.patch("/transactions/{id}")
async def update_transaction(
    id: Annotated[int | None, Path(title="Transaction ID", gt=0)],
    data: Annotated[dict, TransactionPatch]
):
    """
    Update a transaction in the database

    @param id: Transaction ID
    @param data: Transaction data

    @return: Updated transaction
    """
    pass
