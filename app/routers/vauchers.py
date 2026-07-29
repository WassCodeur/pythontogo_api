from fastapi import APIRouter, Depends, HTTPException
from app.schemas.models import VoucherCreate, VoucherUpdate, MessageResponse, VaucherGenerated
from app.utils.vauchers import generate_voucher_code, get_voucher_by_code, update_voucher, delete_voucher
from app.database.connection import get_db_connection


api_router = APIRouter(
    prefix="/vouchers",
    tags=["Vouchers"],
    responses={404: {"description": "Not found"}},
)


@api_router.post("/", response_model=VaucherGenerated, status_code=201)
async def create_voucher(voucher: VoucherCreate, db=Depends(get_db_connection)):
    """
    Create a new voucher with a unique code.
    """
    try:
        voucher_data = voucher.model_dump(exclude_unset=True)
        voucher_code = await generate_voucher_code(db, voucher_data)
        return VaucherGenerated(code=voucher_code)

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Something went wrong while creating the voucher code.")


@api_router.get("/")
async def get_voucher(couponCode: str, db=Depends(get_db_connection)):
    """
    Retrieve a voucher by its code.
    """
    try:
        voucher = await get_voucher_by_code(db, voucher_code=couponCode)
        if not voucher:
            raise HTTPException(status_code=404, detail="Voucher not found")
        return voucher

    except Exception as e:
        if isinstance(e, HTTPException):
            raise e
        raise HTTPException(
            status_code=500, detail="Something went wrong while retrieving the voucher.")
