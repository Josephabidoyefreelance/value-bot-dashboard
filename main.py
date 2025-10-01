from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
import os

app = FastAPI()

# Serve static files (CSS/JS if you add any later)
if not os.path.exists("static"):
    os.mkdir("static")
app.mount("/static", StaticFiles(directory="static"), name="static")

# Serve bets.html
@app.get("/")
async def dashboard():
    return FileResponse("templates/bets.html")
