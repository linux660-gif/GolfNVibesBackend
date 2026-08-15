# from fastapi import APIRouter, HTTPException, status
# from app.schemas.payment_schema import MpesaCreatePayment, PayPalCreateOrder
# from app.clients.mpesa import MpesaClient
# from app.clients.paypal import PayPalClient
#
#
# router = APIRouter(prefix="/payments",
#     tags=["Payments"])
#
# @router.post("/paypal/create-order")
# async def create_order(order: PayPalCreateOrder):
#
#     paypal = PayPalClient()
#
#     return await paypal.create_order(
#         order.payload
#     )
#
#
# @router.post("/paypal/capture-order/{order_id}")
# async def capture_order(order_id: str):
#
#     paypal = PayPalClient()
#
#     return await paypal.capture_order(
#         order_id
#     )
#
#
# @router.post("/mpesa/initiate-stk-push")
# async def initiate_stk_push(
#     payment: MpesaCreatePayment
# ):
#
#     mpesa = MpesaClient()
#
#     return await mpesa.initiate_stk_push(
#         payment.payload
#     )