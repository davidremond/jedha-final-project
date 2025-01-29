from fastapi import APIRouter

router = APIRouter()

@router.get("/predict2")
async def predict2():
    return "todo"