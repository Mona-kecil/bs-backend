from typing import Annotated
from datetime import datetime
from uuid import uuid4
from enum import Enum

from fastapi import APIRouter, Path, HTTPException
from pydantic import BaseModel

from app.models.database import get_connection

router = APIRouter()


class PaymentMethod(str, Enum):
    KIOSK = 'kiosk'
    MANUAL = 'manual'
    MOBILE = 'mobile'


class PaymentPost(BaseModel):
    license_plate: str
    payment_method: PaymentMethod
    amount: int
    payment_time: datetime


@router.get('/payments/{license_plate}')
def get_payment_by_license_plate(
        license_plate: Annotated[str, Path(title='License Plate')]
):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            select payments.*
            from payments as payments
            join parking_sessions as session
            on payments.parking_session_id = session.id
            where session.license_plate = ?
            and payments.deleted_at is null
            ''', (license_plate,))
            row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail={
                    'message': 'data not found',
                    'license_plate': license_plate
                }
            )

        return {
            'message': 'success',
            'data': dict(row)
        }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to fetch data: {str(e)}'
        )


@router.post('/payments')
def create_payment(
    data: PaymentPost
):
    try:
        payment_id = str(uuid4())
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            select id from parking_sessions
            where license_plate = ?
            and exit_time is null
            and deleted_at is null
            ''', (data.license_plate,))

            session = cursor.fetchone()
            if not session:
                raise HTTPException(
                    status_code=404,
                    detail='Parking session doesn\'t exist'
                )

            cursor.execute('''
            insert into payments(
                id,
                parking_session_id,
                payment_method,
                amount,
                payment_time
            )
            values (?,?,?,?,?)
            ''', (
                payment_id,
                session['id'],
                data.payment_method,
                data.amount,
                data.payment_time
            )
            )
            conn.commit()

            return {
                'message': 'success',
                'payment_id': payment_id,
                'license_plate': data.license_plate,
                'payment_time': data.payment_time
            }

    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to create payment: {str(e)}'
        )


@router.delete('/payments/{license_plate}')
def delete_payments(
    license_plate: Annotated[str, Path(
        title='License Plate'
    )]
):
    try:
        deleted_time = datetime.now().isoformat()
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            update payments
            set deleted_at = ?
            where parking_session_id in (
                select id
                from parking_sessions
                where license_plate = ?
            )
            ''', (deleted_time, license_plate))
            conn.commit()

        return {
            'message': 'success',
            'license_plate': license_plate,
            'deleted_at': deleted_time
        }
    except Exception as e:
        raise HTTPException(
            status=400,
            detail=f'Failed to delete data: {str(e)}'
        )
