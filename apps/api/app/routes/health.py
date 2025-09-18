from fastapi import APIRouter


router = APIRouter()

HEALTH_QUESTIONS = [
    {"id": i, "text": f"Health question {i}"} for i in range(1, 19)
]


@router.get("")
async def get_questions():
    return HEALTH_QUESTIONS

