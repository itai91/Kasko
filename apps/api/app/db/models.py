"""Mongo logical models (not ODM), helpers for normalization."""
from datetime import datetime
from typing import Any, Dict


def new_lead_doc(data: Dict[str, Any]) -> Dict[str, Any]:
    doc = {
        **data,
        "created_at": datetime.utcnow(),
        "status": data.get("status", "pending"),
        "offers": data.get("offers", []),
        "source": data.get("source", "web"),
    }
    return doc

