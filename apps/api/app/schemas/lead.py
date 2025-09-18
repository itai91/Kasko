from typing import List
from pydantic import BaseModel

from .mortgage import Mortgage
from .person import Person


class LeadCreate(BaseModel):
    mortgage: Mortgage
    insured_list: List[Person]
    contact_agreed: bool


class LeadOut(BaseModel):
    lead_id: str

