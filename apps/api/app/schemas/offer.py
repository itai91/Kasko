from pydantic import BaseModel


class Offer(BaseModel):
    company_id: str
    company_name: str
    first_month_premium: float
    average_monthly_premium: float
    total_premium: float
    max_monthly_premium: float

