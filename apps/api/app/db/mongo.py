from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase, AsyncIOMotorCollection

from ..config import settings

_client: Optional[AsyncIOMotorClient] = None
_db: Optional[AsyncIOMotorDatabase] = None


async def connect_to_mongo() -> None:
    global _client, _db
    if _client is None:
        _client = AsyncIOMotorClient(str(settings.MONGO_URI))
        _db = _client[settings.MONGO_DB]
        await _ensure_indexes()


async def close_mongo_connection() -> None:
    global _client
    if _client is not None:
        _client.close()
        _client = None


def get_db() -> AsyncIOMotorDatabase:
    assert _db is not None, "MongoDB is not initialized"
    return _db


def leads_collection() -> AsyncIOMotorCollection:
    return get_db()["leads"]


def companies_collection() -> AsyncIOMotorCollection:
    return get_db()["companies"]


async def _ensure_indexes() -> None:
    # Basic indexes: created_at, and a compound on phone+id_number for duplicates
    col = leads_collection()
    await col.create_index("created_at")
    await col.create_index([("insured_list.phone", 1), ("insured_list.id_number", 1)])

