from typing import List

from ..db.mongo import companies_collection
from .calculator import compute_offers_across_companies


async def list_companies() -> List[dict]:
    col = companies_collection()
    docs = col.find({}, {"_id": 0})
    return [doc async for doc in docs]


async def compute_offers_for_all_companies(
    loan_amount: float,
    term_months: int,
    age: int,
    gender: str,
    is_smoker: bool,
):
    companies = await list_companies()
    if not companies:
        # Fallback default companies if DB empty
        companies = [
            {"id": "hchsra", "name": "Hachshara", "logo_url": "https://example.com/hchsra.png"},
            {"id": "migdal", "name": "Migdal", "logo_url": "https://example.com/migdal.png"},
        ]
    return compute_offers_across_companies(
        loan_amount, term_months, age, gender, is_smoker, companies
    )

