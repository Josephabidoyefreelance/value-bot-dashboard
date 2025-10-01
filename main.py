from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import JSONResponse
import sqlite3
from datetime import datetime
import threading
import time

app = FastAPI()

# Database
conn = sqlite3.connect("bets.db", check_same_thread=False)
cursor = conn.cursor()
cursor.execute("""
CREATE TABLE IF NOT EXISTS bets (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    market TEXT,
    odds REAL,
    probability REAL,
    edge REAL,
    stake REAL,
    result TEXT
)
""")
conn.commit()

# Templates
templates = Jinja2Templates(directory="templates")

# Dummy endpoints
def dummy_ps3838():
    return [
        {"market": "TeamA vs TeamB", "odds": 2.0, "probability": 0.55},
        {"market": "TeamC vs TeamD", "odds": 1.8, "probability": 0.6}
    ]

def dummy_asianodds():
    return [
        {"market": "TeamG vs TeamH", "odds": 2.1, "probability": 0.52},
        {"market": "TeamI vs TeamJ", "odds": 1.9, "probability": 0.58}
    ]

# Function to log bets
def run_bets_logic():
    all_odds = dummy_ps3838() + dummy_asianodds()
    for bet in all_odds:
        edge = bet["probability"] - 1 / bet["odds"]
        stake = 10.0
        result = "OPEN"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        cursor.execute(
            "INSERT INTO bets (timestamp, market, odds, probability, edge, stake, result) VALUES (?, ?, ?, ?, ?, ?, ?)",
            (timestamp, bet["market"], bet["odds"], bet["probability"], edge, stake, result)
        )
        conn.commit()

# Background thread function
def auto_run_bets():
    while True:
        run_bets_logic()
        time.sleep(120)  # 2 minutes

# Start background thread on app startup
@app.on_event("startup")
def start_background_tasks():
    thread = threading.Thread(target=auto_run_bets, daemon=True)
    thread.start()

# Routes
@app.get("/")
def read_root(request: Request):
    return templates.TemplateResponse("bets.html", {"request": request, "bets": []})

@app.get("/bets")
def get_bets():
    cursor.execute("SELECT * FROM bets ORDER BY id DESC")
    bets = cursor.fetchall()
    return JSONResponse(bets)

@app.get("/dashboard")
def dashboard(request: Request):
    cursor.execute("SELECT * FROM bets ORDER BY id DESC")
    bets = cursor.fetchall()
    return templates.TemplateResponse("bets.html", {"request": request, "bets": bets})

# ====== NEW API ENDPOINTS ======
@app.get("/api/bets")
def api_bets():
    cursor.execute("SELECT * FROM bets ORDER BY id DESC")
    bets = cursor.fetchall()
    return {"bets": bets}

@app.get("/api/kpis")
def api_kpis():
    cursor.execute("SELECT SUM(stake) as total_stake, SUM(edge) as total_edge FROM bets")
    row = cursor.fetchone()
    bankroll = 1000  # dummy
    roi = round((row[1] or 0) * 100, 2)
    clv = round((row[1] or 0), 2)
    turnover = round((row[0] or 0), 2)
    return {
        "bankroll": bankroll,
        "roi": roi,
        "clv": clv,
        "turnover": turnover
    }
