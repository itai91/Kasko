from fastapi import APIRouter

from ..db.mongo import companies_collection


router = APIRouter()


@router.get("")
async def get_companies():
    col = companies_collection()
    docs = col.find({}, {"_id": 0})
    companies = [doc async for doc in docs]
    if not companies:
        companies = [
            {"id": "hchsra", "name": "Hachshara", "logo_url": "https://example.com/hchsra.png"},
            {"id": "migdal", "name": "Migdal", "logo_url": "https://example.com/migdal.png"},
        ]
    return companies

