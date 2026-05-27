from fastapi import APIRouter, Depends, HTTPException, status


api_router = APIRouter(prefix="/api/v2/checkout", tags=["notifications"])


@api_router.get("/payment-success")
def payment_success():
    return {"message": "Payment successful"}


@api_router.get("/payment-cancel")
def payment_cancel():
    return {"message": "Payment cancelled"}
