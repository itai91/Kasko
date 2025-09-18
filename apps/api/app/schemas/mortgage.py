from datetime import date
from typing import List, Literal
from pydantic import BaseModel, PositiveFloat, condecimal


class MortgageTrack(BaseModel):
    amount: PositiveFloat
    interest_type: Literal["fixed", "variable", "prime"]
    annual_rate: condecimal(gt=0, max_digits=5, decimal_places=2)
    start_date: date
    end_date: date
    loan_type: Literal["spitzer", "bullet", "balloon"]


class Mortgage(BaseModel):
    start_date: date
    bank_name: str
    tracks: List[MortgageTrack]

