from typing import Any
from bson import ObjectId
from fastapi import APIRouter, HTTPException

from ..db.mongo import leads_collection
from ..db.models import new_lead_doc
from ..schemas.lead import LeadCreate, LeadOut
from ..tasks import calculate_offers_task


router = APIRouter()


@router.post("", status_code=201, response_model=LeadOut)
async def create_lead(payload: LeadCreate):
    col = leads_collection()
    doc = new_lead_doc(payload.model_dump())
    result = await col.insert_one(doc)
    lead_id = str(result.inserted_id)
    # Trigger background task
    try:
        calculate_offers_task.delay(lead_id)
    except Exception:
        # In dev without broker, ignore
        pass
    return LeadOut(lead_id=lead_id)


@router.get("/{lead_id}")
async def get_lead(lead_id: str) -> Any:
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead_id")
    col = leads_collection()
    doc = await col.find_one({"_id": ObjectId(lead_id)})
    if not doc:
        raise HTTPException(status_code=404, detail="Lead not found")
    doc["id"] = str(doc.pop("_id"))
    return doc


@router.post("/purchase")
async def purchase(
    lead_id: str,
    card_token: str,
    address_line: str | None = None,
    city: str | None = None,
    zip_code: str | None = None,
):
    # Placeholder – real implementation integrates with payment provider
    if not ObjectId.is_valid(lead_id):
        raise HTTPException(status_code=400, detail="Invalid lead_id")
    return {"status": "ok", "lead_id": lead_id}

