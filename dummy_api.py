from fastapi import FastAPI
from fastapi.responses import JSONResponse
from datetime import datetime
import random

app = FastAPI()

# Dummy odds
def dummy_bets():
    markets = ["TeamA vs TeamB", "TeamC vs TeamD", "TeamG vs TeamH", "TeamI vs TeamJ"]
    bets = []
    for market in markets:
        odds = round(random.uniform(1.5, 2.5), 2)
        probability = round(random.uniform(0.4, 0.7), 2)
        bets.append({"market": market, "odds": odds, "probability": probability})
    return bets

@app.get("/run-bets")
def run_bets():
    dummy_data = dummy_bets()
    logged_bets = []
    for bet in dummy_data:
        edge = bet["probability"] - 1/bet["odds"]
        stake = 10.0
        result = "SHADOW"
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        logged_bets.append([0, timestamp, bet["market"], bet["odds"], bet["probability"], edge, stake, result])
    return JSONResponse(logged_bets)
