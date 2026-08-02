from typing import Any, Dict

from pydantic import BaseModel


class PaymentCreate(BaseModel):
    headers: Dict[str, str]



class PayPalCreateOrder(PaymentCreate):
    def __init__(self, /, **data: Any):
        super().__init__(null, data)
        self.payload = None

    pass

class PayPalOrderPayload(BaseModel):
    intent: str
    purchase_units: list

class PayPalCaptureOrder(PaymentCreate):
    order_id: str

class MpesaCreatePayment(PaymentCreate):
    pass

class MpesaStkPush(PaymentCreate):
    phone_number: str
    amount : int

    
