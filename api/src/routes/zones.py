from fastapi import APIRouter

router = APIRouter()

@router.get("/zones")
async def zones():
    return "todo"