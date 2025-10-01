from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
import json
import math
import logging

app = FastAPI()
templates = Jinja2Templates(directory="templates")
app.mount("/static", StaticFiles(directory="static"), name="static")

logging.basicConfig(filename="app.log", level=logging.INFO)

BANKROLL_START = 1000
SHADOW_MODE = True  # toggle this True/False

def kelly_stake(bankroll, odds, edge):
    return bankroll * edge / (odds - 1)

def calculate_metrics(data, bankroll_start=BANKROLL_START):
    bankroll = bankroll_start
    roi_total = 0
    clv_total = 0
    for bet in data:
        stake = bet.get("bet_amount", 10)  # flat stake
        if SHADOW_MODE:
            logging.info(f"Shadow bet: {bet['match']} - {stake}$")
        # result calc
        if bet["result"] == "win":
            profit = stake * (bet["odds_close"] - 1)
        else:
            profit = -stake
        bankroll += profit
        roi_total += profit / stake
        clv_total += (bet["odds_close"] - bet["odds_open"]) / bet["odds_open"]
        bet["profit"] = round(profit, 2)
        bet["bankroll_after"] = round(bankroll, 2)
        bet["clv"] = round((bet["odds_close"] - bet["odds_open"]) / bet["odds_open"] * 100, 2)
    roi_avg = round((roi_total / len(data)) * 100, 2)
    clv_avg = round((clv_total / len(data)) * 100, 2)
    return data, round(bankroll,2), roi_avg, clv_avg

@app.get("/")
def dashboard(request: Request):
    try:
        with open("mock_data.json") as f:
            bets = json.load(f)
        bets, bankroll, roi, clv = calculate_metrics(bets)
        return templates.TemplateResponse("bets.html", {
            "request": request,
            "bets": bets,
            "bankroll": bankroll,
            "roi": roi,
            "clv": clv,
            "shadow_mode": SHADOW_MODE
        })
    except Exception as e:
        logging.error(f"Error loading dashboard: {e}")
        return {"error": "Something went wrong"}
