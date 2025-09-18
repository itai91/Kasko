from fastapi import APIRouter

from .companies import router as companies_router
from .premium import router as premium_router
from .offers import router as offers_router
from .leads import router as leads_router
from .health import router as health_router


api_router = APIRouter()
api_router.include_router(companies_router, prefix="/companies", tags=["companies"])
api_router.include_router(premium_router, prefix="/premium", tags=["premium"])
api_router.include_router(offers_router, prefix="/offers", tags=["offers"])
api_router.include_router(leads_router, prefix="/leads", tags=["leads"])
api_router.include_router(health_router, prefix="/questions", tags=["health"])  # optional

