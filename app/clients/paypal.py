# from fastapi import HTTPException, status
# import httpx
#
# from app.core.config import settings
#
#
# class PayPalClient:
#
#     def __init__(self):
#         self.base_url = settings.paypal_base_url
#         self.timeout = 30.0
#
#     @staticmethod
#     def _auth_headers(token: str) -> dict:
#         return {
#             "Authorization": f"Bearer {token}",
#             "Content-Type": "application/json",
#         }
#
#     async def get_access_token(
#         self,
#         client: httpx.AsyncClient
#     ) -> str:
#
#         url = f"{self.base_url}/v1/oauth2/token"
#
#         try:
#             response = await client.post(
#                 url,
#                 auth=(
#                     settings.paypal_client_id,
#                     settings.paypal_client_secret
#                 ),
#                 data={
#                     "grant_type": "client_credentials"
#                 },
#                 headers={
#                     "Content-Type":
#                     "application/x-www-form-urlencoded"
#                 }
#             )
#
#             response.raise_for_status()
#
#             return response.json()["access_token"]
#
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_502_BAD_GATEWAY,
#                 detail=f"PayPal authentication failed: {e.response.text}"
#             )
#
#         except httpx.RequestError:
#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail="Unable to connect to PayPal."
#             )
#
#     async def create_order(
#         self,
#         payload: dict
#     ):
#
#         async with httpx.AsyncClient(
#             timeout=self.timeout
#         ) as client:
#
#             token = await self.get_access_token(client)
#
#             url = f"{self.base_url}/v2/checkout/orders"
#
#             try:
#
#                 response = await client.post(
#                     url,
#                     json=payload,
#                     headers=self._auth_headers(token)
#                 )
#
#                 response.raise_for_status()
#
#                 return response.json()
#
#             except httpx.HTTPStatusError as e:
#                 raise HTTPException(
#                     status_code=status.HTTP_502_BAD_GATEWAY,
#                     detail=f"Failed to create PayPal order: {e.response.text}"
#                 )
#
#             except httpx.RequestError:
#                 raise HTTPException(
#                     status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                     detail="Unable to connect to PayPal."
#                 )
#
#     async def capture_order(
#         self,
#         order_id: str
#     ):
#
#         async with httpx.AsyncClient(
#             timeout=self.timeout
#         ) as client:
#
#             token = await self.get_access_token(client)
#
#             url = (
#                 f"{self.base_url}"
#                 f"/v2/checkout/orders/{order_id}/capture"
#             )
#
#             try:
#
#                 response = await client.post(
#                     url,
#                     headers=self._auth_headers(token)
#                 )
#
#                 response.raise_for_status()
#
#                 return response.json()
#
#             except httpx.HTTPStatusError as e:
#                 raise HTTPException(
#                     status_code=status.HTTP_502_BAD_GATEWAY,
#                     detail=f"Capture failed: {e.response.text}"
#                 )
#
#             except httpx.RequestError:
#                 raise HTTPException(
#                     status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                     detail="Unable to connect to PayPal."
#                 )