from typing import Annotated

from fastapi import APIRouter, Query, Path

from app.services import supabase_service

router = APIRouter()


@router.get('/vehicles')
async def get_vehicles(
    skip: Annotated[int, Query(title='Offset', gt=0)] = 0,
    limit: Annotated[int, Query(title='Limit', gt=0)] = 100
):
    response = supabase_service.fetch_table_data('vehicles')
    return response.data


@router.get('/vehicles/{id}')
async def get_vehicle_by_id(
    id: Annotated[int, Path()]
):
    return "Not implemented"
