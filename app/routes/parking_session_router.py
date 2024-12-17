from typing import Annotated
from datetime import datetime
from uuid import uuid4

from fastapi import APIRouter, Query, Path, HTTPException
from pydantic import BaseModel

from app.models.database import get_connection


router = APIRouter()


class SessionPost(BaseModel):
    license_plate: str
    entry_time: datetime


class SessionPatch(BaseModel):
    exit_time: datetime


@router.get('/sessions')
def get_sessions(
        skip: Annotated[int, Query(title="Offset", ge=0)] = 0,
        limit: Annotated[int, Query(title="Limit", gt=0, le=100)] = 10
):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            select * from parking_sessions
            where deleted_at is null
            limit ?
            offset ?
            ''', (limit, skip))
            rows = cursor.fetchall()
        return {
            'message': 'success',
            'data': [dict(row) for row in rows]
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to fetch data: {str(e)}'
        )


@router.get('/sessions/{license_plate}')
def get_session_by_license_plate(
    license_plate: Annotated[str, Path(title='License Plate')]
):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            select * from parking_sessions
            where license_plate = ? and deleted_at is null
            ''', (license_plate,))
            row = cursor.fetchone()

        if row is None:
            raise HTTPException(
                status_code=404,
                detail={
                    'message': 'Vehicle not found!',
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


@router.post('/sessions')
def post_session(
    data: SessionPost
):
    try:
        session_id = str(uuid4())
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            insert into parking_sessions(id, license_plate, entry_time)
            values(?,?,?)
            ''', (session_id, data.license_plate, data.entry_time.isoformat()))
            conn.commit()

        return {
            'message': 'Parking session created successfully',
            'session_id': session_id,
            'license_plate': data.license_plate,
            'entry_time': data.entry_time
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to create parking session: {str(e)}'
        )


@router.patch('/sessions/{license_plate}')
def update_session(
    license_plate: Annotated[str | None, Path(
        title='Vehicle\'s license plate')],
    data: SessionPatch
):
    try:
        with get_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
            update parking_sessions
            set exit_time = ?, deleted_at = ?
            where license_plate = ?
            ''', (
                data.exit_time.isoformat(),
                datetime.now().isoformat(),
                license_plate)
            )
            conn.commit()
        return {
            'message': 'success',
            'license_plate': license_plate,
            'exit_time': data.exit_time
        }
    except Exception as e:
        raise HTTPException(
            status_code=400,
            detail=f'Failed to update: {str(e)}'
        )
