"""Alert endpoints."""
from fastapi import APIRouter
router = APIRouter()
@router.get("")
async def list_alerts():
    return {"message": "Alerts endpoint"}
