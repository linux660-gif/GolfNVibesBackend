# from fastapi import HTTPException, status
# import httpx
# from app.core.config import settings
#
#
# class MpesaClient:
#
#     def __init__(self):
#         self.base_url = settings.mpesa_base_url
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
#         url = (
#             f"{self.base_url}"
#             "/oauth/v1/generate"
#             "?grant_type=client_credentials"
#         )
#
#         try:
#
#             response = await client.get(
#                 url,
#                 auth=(
#                     settings.mpesa_consumer_key,
#                     settings.mpesa_consumer_secret
#                 )
#             )
#
#             response.raise_for_status()
#
#             return response.json()["access_token"]
#
#         except httpx.HTTPStatusError as e:
#             raise HTTPException(
#                 status_code=status.HTTP_502_BAD_GATEWAY,
#                 detail=f"Mpesa auth failed: {e.response.text}"
#             )
#
#         except httpx.RequestError:
#             raise HTTPException(
#                 status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                 detail="Unable to connect to Mpesa."
#             )
#
#     async def initiate_stk_push(
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
#             url = (
#                 f"{self.base_url}"
#                 "/mpesa/stkpush/v1/processrequest"
#             )
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
#                     detail=f"STK Push failed: {e.response.text}"
#                 )
#
#             except httpx.RequestError:
#                 raise HTTPException(
#                     status_code=status.HTTP_503_SERVICE_UNAVAILABLE,
#                     detail="Unable to connect to Mpesa."
#                 )