from fastapi import APIRouter

from ..services.offers import compute_offers_for_all_companies


router = APIRouter()


@router.get("")
async def get_offers(
    loan_amount: float,
    term_months: int,
    age: int,
    gender: str,
    is_smoker: bool,
):
    offers = await compute_offers_for_all_companies(
        loan_amount, term_months, age, gender, is_smoker
    )
    return offers

