from fastapi import APIRouter

from api.documents.router import router as document_router
from api.message.router import router as message_router

api_router = APIRouter()

include_api = api_router.include_router

routers = (
   (document_router, "document", "document"),
   (message_router, "message", "message"),
)

for router_item in routers:
   router, prefix, tag = router_item

   if tag:
       include_api(router, prefix=f"/{prefix}", tags=[tag])
   else:
       include_api(router, prefix=f"/{prefix}")
