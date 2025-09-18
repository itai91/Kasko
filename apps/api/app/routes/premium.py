from fastapi import APIRouter

from ..schemas.premium import PremiumRequest, PremiumResponse
from ..services.calculator import compute_company_premium_first_month


router = APIRouter()


@router.get("")
async def get_premium(
    loan_amount: float,
    term_months: int,
    age: int,
    gender: str,
    is_smoker: bool,
    company_id: str,
):
    req = PremiumRequest(
        loan_amount=loan_amount,
        term_months=term_months,
        age=age,
        gender=gender,  # type: ignore[arg-type]
        is_smoker=is_smoker,
        company_id=company_id,
    )
    value = compute_company_premium_first_month(
        req.loan_amount, req.term_months, req.age, req.gender, req.is_smoker, req.company_id
    )
    return PremiumResponse(monthly_premium=value)

