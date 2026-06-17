"""Payment endpoints."""
from fastapi import APIRouter
router = APIRouter()
@router.post("")
async def create_payment():
    return {"message": "Payments endpoint"}
