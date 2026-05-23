from fastapi import APIRouter, Depends, Request, Header
from sqlalchemy.orm import Session

from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import CheckoutSession, SubscriptionStatus

router = APIRouter()


@router.post("/create-checkout-session", response_model=CheckoutSession)
def create_checkout_session(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Creates a Stripe Checkout session for the current user.
    Full implementation included in the complete package.
    """
    raise NotImplementedError("Available in the full package")


@router.get("/success")
def checkout_success(session_id: str, db: Session = Depends(get_db)):
    """
    Handles Stripe redirect after successful payment.
    Full implementation included in the complete package.
    """
    raise NotImplementedError("Available in the full package")


@router.get("/cancel")
def checkout_cancel():
    return {"message": "Checkout cancelled"}


@router.get("/status", response_model=SubscriptionStatus)
def get_subscription_status(current_user: User = Depends(get_current_user)):
    """
    Returns current subscription status for the authenticated user.
    Full implementation included in the complete package.
    """
    raise NotImplementedError("Available in the full package")


@router.post("/cancel-subscription")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    """
    Cancels subscription at end of billing period.
    Full implementation included in the complete package.
    """
    raise NotImplementedError("Available in the full package")


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db),
):
    """
    Handles Stripe webhook events (subscription deleted, payment failed).
    Full implementation included in the complete package.
    """
    raise NotImplementedError("Available in the full package")