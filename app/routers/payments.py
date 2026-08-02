from fastapi import APIRouter, HTTPException, status
from app.schemas.payment_service import MpesaCreatePayment, PayPalCreateOrder, PayPalCaptureOrder
from app.clients.mpesa import MpesaClient
from app.clients.paypal import PayPalClient


router = APIRouter()

@router.post("/paypal/create-order")
async def create_order(order: PayPalCreateOrder):

    paypal = PayPalClient()

    return await paypal.create_order(
        order.payload
    )


@router.post("/paypal/capture-order/{order_id}")
async def capture_order(order_id: str):

    paypal = PayPalClient()

    return await paypal.capture_order(
        order_id
    )


@router.post("/mpesa/initiate-stk-push")
async def initiate_stk_push(
    payment: MpesaCreatePayment
):

    mpesa = MpesaClient()

    return await mpesa.initiate_stk_push(
        payment.payload
    )