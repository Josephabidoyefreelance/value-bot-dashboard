from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from fastapi.responses import HTMLResponse

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/bets.html", response_class=HTMLResponse)
async def get_bets(request: Request):
    return templates.TemplateResponse("bets.html", {"request": request})
