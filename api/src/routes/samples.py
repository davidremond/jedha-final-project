from fastapi import APIRouter

router = APIRouter()

@router.get("/samples")
async def samples():
    return "todo"