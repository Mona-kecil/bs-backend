from fastapi import APIRouter

router = APIRouter()


@router.post('/manual-actions')
async def manual_actions():
    """
    This endpoint is used to manually trigger actions such as:
    - Manually let a vehicle enter/exit the parking lot
    - Manually update the payment status of a vehicle
    - Maybe more, but I still need to figure out what I want to do with it
    """
    return "not implemented yet"


@router.get('/overdue-payments')
async def get_overdue_payments():
    """
    This endpoint is used to get a list of overdue payments
    """
    return "not implemented yet"


@router.get('/dashboard')
async def get_dashboard():
    """
    Fetch aggregated data for the dashboard
    """
    return "not implemented yet"
