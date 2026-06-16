from fastapi import APIRouter, Request
from fastapi.templating import Jinja2Templates

from core.config import TEMPLATE_DIR

router = APIRouter(tags=["pages"])

templates = Jinja2Templates(directory=TEMPLATE_DIR)


@router.get("/")
async def page_index(request: Request):
    return templates.TemplateResponse(request, "index.html")


@router.get("/editor")
async def page_editor(request: Request):
    return templates.TemplateResponse(request, "rehab_rule_editor.html")
