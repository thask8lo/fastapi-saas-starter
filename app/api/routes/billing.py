from fastapi import APIRouter, Depends, HTTPException, Request, Header
from sqlalchemy.orm import Session
import stripe

from app.core.config import settings
from app.core.database import get_db
from app.core.security import get_current_user
from app.models.user import User
from app.schemas.user import CheckoutSession, SubscriptionStatus

router = APIRouter()
stripe.api_key = settings.STRIPE_SECRET_KEY


@router.post("/create-checkout-session", response_model=CheckoutSession)
def create_checkout_session(
    request: Request,
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if current_user.is_subscribed:
        raise HTTPException(status_code=400, detail="Already subscribed")

    # Create or retrieve Stripe customer
    if not current_user.stripe_customer_id:
        customer = stripe.Customer.create(email=current_user.email)
        current_user.stripe_customer_id = customer.id
        db.commit()

    session = stripe.checkout.Session.create(
        customer=current_user.stripe_customer_id,
        payment_method_types=["card"],
        line_items=[{"price": settings.STRIPE_PRICE_ID, "quantity": 1}],
        mode="subscription",
        success_url=f"{request.base_url}api/billing/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{request.base_url}api/billing/cancel",
        metadata={"user_id": str(current_user.id)},
    )

    return CheckoutSession(checkout_url=session.url)


@router.get("/success")
def checkout_success(session_id: str, db: Session = Depends(get_db)):
    session = stripe.checkout.Session.retrieve(session_id)
    user = db.query(User).filter(User.id == int(session.metadata["user_id"])).first()
    if user:
        user.is_subscribed = True
        user.subscription_status = "active"
        user.stripe_subscription_id = session.subscription
        db.commit()
    return {"message": "Subscription activated successfully!"}


@router.get("/cancel")
def checkout_cancel():
    return {"message": "Checkout cancelled"}


@router.get("/status", response_model=SubscriptionStatus)
def get_subscription_status(current_user: User = Depends(get_current_user)):
    return SubscriptionStatus(
        is_subscribed=current_user.is_subscribed,
        subscription_status=current_user.subscription_status,
        stripe_subscription_id=current_user.stripe_subscription_id,
    )


@router.post("/cancel-subscription")
def cancel_subscription(
    current_user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
):
    if not current_user.stripe_subscription_id:
        raise HTTPException(status_code=400, detail="No active subscription")

    stripe.Subscription.modify(
        current_user.stripe_subscription_id,
        cancel_at_period_end=True,
    )

    current_user.subscription_status = "cancel_at_period_end"
    db.commit()
    return {"message": "Subscription will be cancelled at end of billing period"}


@router.post("/webhook")
async def stripe_webhook(
    request: Request,
    stripe_signature: str = Header(None),
    db: Session = Depends(get_db),
):
    payload = await request.body()
    try:
        event = stripe.Webhook.construct_event(
            payload, stripe_signature, settings.STRIPE_WEBHOOK_SECRET
        )
    except Exception:
        raise HTTPException(status_code=400, detail="Invalid webhook signature")

    if event["type"] == "customer.subscription.deleted":
        subscription = event["data"]["object"]
        user = db.query(User).filter(
            User.stripe_subscription_id == subscription["id"]
        ).first()
        if user:
            user.is_subscribed = False
            user.subscription_status = "canceled"
            db.commit()

    elif event["type"] == "invoice.payment_failed":
        subscription_id = event["data"]["object"].get("subscription")
        user = db.query(User).filter(
            User.stripe_subscription_id == subscription_id
        ).first()
        if user:
            user.subscription_status = "past_due"
            db.commit()

    return {"received": True}
