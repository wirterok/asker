from contextlib import asynccontextmanager

from fastapi import FastAPI, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
import uvicorn

from api.endpoints import api_router
from ml import llm
from api.message.dependencies import get_message_crud, MessageCRUD

from . import settings

@asynccontextmanager
async def lifespan(app: FastAPI):
    llm.load_model()
    await llm.update_content()
    yield

app = FastAPI(
   title=settings.project_name,
   version=settings.version,
   openapi_url=f"{settings.api_v1_prefix}/openapi.json",
   debug=settings.debug,
   lifespan=lifespan
)

templates = Jinja2Templates(directory="templates")

@app.get("/", response_class=HTMLResponse)
async def chat(request: Request, messages: MessageCRUD = Depends(get_message_crud)):
   messages = await messages.list()
   messages = [x.to_html_data() for x in messages]
   return templates.TemplateResponse("index.html", {"request": request, "messages": messages})

app.include_router(api_router, prefix=settings.api_v1_prefix)

app.mount("/static/css", StaticFiles(directory="static/css"), name="css")
app.mount("/static/js", StaticFiles(directory="static/js"), name="js")

if __name__ == '__main__':
   uvicorn.run("main:app", port=8080, host="0.0.0.0", reload=True)