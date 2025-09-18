from celery import Celery
import logging
from bson import ObjectId

from .config import settings
from pymongo import MongoClient
from .services.offers import compute_offers_for_all_companies
from .services.mailer import send_email

logger = logging.getLogger(__name__)


celery_app = Celery(
    "kasko_tasks",
    broker=settings.CELERY_BROKER_URL,
    backend=settings.CELERY_RESULT_BACKEND,
)


@celery_app.task(name="calculate_offers_task")
def calculate_offers_task(lead_id: str):
    """Fetch lead, compute offers, update DB and send mail."""
    try:
        client = MongoClient(str(settings.MONGO_URI))
        db = client[settings.MONGO_DB]
        leads = db["leads"]
        lead = leads.find_one({"_id": ObjectId(lead_id)})  # type: ignore[arg-type]
        if not lead:
            logger.warning("Lead %s not found for offers task", lead_id)
            return
        # Simplified: use first insured's data
        insured = (lead.get("insured_list") or [{}])[0]
        # Compute age from date_of_birth if present
        from datetime import date, datetime
        dob_raw = insured.get("date_of_birth")
        age = 30
        if dob_raw:
            try:
                dob = dob_raw if isinstance(dob_raw, date) else datetime.fromisoformat(dob_raw).date()
                today = date.today()
                age = today.year - dob.year - ((today.month, today.day) < (dob.month, dob.day))
            except Exception:
                age = 30
        gender = insured.get("gender") or "male"
        is_smoker = insured.get("is_smoker") or False
        # Simplify loan using total tracks amount
        mortgage = lead.get("mortgage") or {}
        tracks = mortgage.get("tracks") or []
        loan_amount = sum(float(t.get("amount") or 0) for t in tracks) or 100_000.0
        term_months = 240

        offers = compute_offers_for_all_companies(  # type: ignore[func-returns-value]
            loan_amount, term_months, age, gender, is_smoker
        )
        # If compute_offers_for_all_companies is coroutine (in future), handle accordingly.
        if hasattr(offers, "__await__"):
            import asyncio

            offers = asyncio.get_event_loop().run_until_complete(offers)  # type: ignore

        leads.update_one({"_id": ObjectId(lead_id)}, {"$set": {"offers": offers, "status": "quote_sent"}})

        # Send email (simplified)
        to = lead.get("insured_list", [{}])[0].get("email", "customer@example.com")
        subject = "Your life insurance offers"
        body = f"We computed {len(offers)} offers for your mortgage."
        try:
            import asyncio

            asyncio.get_event_loop().run_until_complete(send_email(to, subject, body))
        except Exception:
            logger.info("Email sending simulated for %s", to)
    except Exception as e:
        logger.exception("calculate_offers_task failed: %s", e)


@celery_app.task(name="send_email_task")
def send_email_task(to: str, subject: str, body: str):
    try:
        import asyncio

        asyncio.get_event_loop().run_until_complete(send_email(to, subject, body))
    except Exception as e:
        logger.exception("send_email_task failed: %s", e)
