from __future__ import annotations
from dataclasses import dataclass
from typing import List, Literal, Dict, Tuple
from math import pow


@dataclass
class SpitzerResult:
    monthly_payment: float
    balance_by_year: List[float]  # remaining balance at the start of each year (1-indexed)


def monthly_payment_spitzer(P: float, annual_rate: float, N: int) -> float:
    r = pow(1 + annual_rate, 1 / 12) - 1
    A = P * r / (1 - pow(1 + r, -N))
    return float(A)


def amortization_spitzer(P: float, annual_rate: float, N: int) -> SpitzerResult:
    r = pow(1 + annual_rate, 1 / 12) - 1
    A = monthly_payment_spitzer(P, annual_rate, N)
    balance = P
    balance_by_year: List[float] = []
    for m in range(1, N + 1):
        interest = balance * r
        principal = A - interest
        balance = max(0.0, balance - principal)
        if m % 12 == 0:
            balance_by_year.append(balance)
    return SpitzerResult(monthly_payment=A, balance_by_year=balance_by_year)


# Minimal in-memory tariff table (example baseline per 100,000 for month 1)
# Key: (age, gender, smoker, company_id)
TariffKey = Tuple[int, Literal["male", "female"], bool, str]


class Tariffs:
    def __init__(self) -> None:
        # A tiny sample; in production, load from DB/Redis/CSV.
        self._base: Dict[TariffKey, float] = {
            (20, "male", False, "hchsra"): 6.25,
            (20, "female", False, "hchsra"): 5.10,
            (30, "male", False, "hchsra"): 7.90,
            (30, "male", True, "hchsra"): 12.50,
        }

    def get(self, age: int, gender: Literal["male", "female"], is_smoker: bool, company_id: str) -> float:
        # Find nearest lower known age; fallback to simple heuristic.
        for delta in range(0, 60):
            key = (max(18, age - delta), gender, is_smoker, company_id)
            if key in self._base:
                return self._base[key]
        # Heuristic baseline if not found
        base = 6.0 if gender == "male" else 5.0
        smoke_factor = 1.6 if is_smoker else 1.0
        age_factor = 1.0 + max(0, age - 20) * 0.02
        return round(base * smoke_factor * age_factor, 2)


tariffs = Tariffs()


def compute_company_premium_first_month(
    loan_amount: float,
    term_months: int,
    age: int,
    gender: Literal["male", "female"],
    is_smoker: bool,
    company_id: str,
) -> float:
    # Use first-year balance factor approximation (month 1 based on starting balance)
    factor = loan_amount / 100_000.0
    base_tariff = tariffs.get(age, gender, is_smoker, company_id)
    return round(base_tariff * factor, 2)


def compute_offers_across_companies(
    loan_amount: float,
    term_months: int,
    age: int,
    gender: Literal["male", "female"],
    is_smoker: bool,
    companies: List[dict],
):
    # Simplified: assume single track, flat annual rate of 4% for amortization balance estimate
    annual_rate = 0.04
    amort = amortization_spitzer(loan_amount, annual_rate, term_months)
    offers = []
    years = max(1, term_months // 12)
    for c in companies:
        cid = c["id"]
        cname = c["name"]
        total = 0.0
        max_month = 0.0
        first_month = 0.0
        for k in range(1, years + 1):
            age_k = age + (k - 1)
            balance_year = amort.balance_by_year[k - 1] if k - 1 < len(amort.balance_by_year) else 0.0
            factor = (balance_year or 0.0) / 100_000.0
            base = tariffs.get(age_k, gender, is_smoker, cid)
            premium_month_k = base * factor
            # 12 months in year k
            total += premium_month_k * 12
            max_month = max(max_month, premium_month_k)
            if k == 1:
                first_month = premium_month_k
        average = total / float(term_months)
        offers.append(
            {
                "company_id": cid,
                "company_name": cname,
                "first_month_premium": round(first_month, 2),
                "average_monthly_premium": round(average, 2),
                "total_premium": round(total, 2),
                "max_monthly_premium": round(max_month, 2),
            }
        )
    return offers

