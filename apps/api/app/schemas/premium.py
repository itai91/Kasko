from typing import Literal
from pydantic import BaseModel, PositiveFloat, conint


class PremiumRequest(BaseModel):
    loan_amount: PositiveFloat
    term_months: conint(ge=12, le=480)
    age: conint(ge=18, le=75)
    gender: Literal["male", "female"]
    is_smoker: bool
    company_id: str


class PremiumResponse(BaseModel):
    monthly_premium: float

