# main.py
from fastapi import FastAPI, Request
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, StreamingResponse
import io, csv, os

app = FastAPI()

# Templates folder path (relative to this file)
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
templates = Jinja2Templates(directory=os.path.join(BASE_DIR, "templates"))

# Serve the dashboard (expects templates/bets.html to exist)
@app.get("/", response_class=HTMLResponse)
async def dashboard(request: Request):
    return templates.TemplateResponse("bets.html", {"request": request})

# Small CSV export endpoint (safe placeholder)
@app.get("/export/csv")
async def export_csv():
    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow(["ID","Timestamp","Sport","Market","Placed Odds","Closing Odds","CLV %","Probability","Edge %","Stake","Result"])
    # Add a sample row so the endpoint returns a file even if frontend handles CSV itself
    writer.writerow([1, "now", "Football", "Sample Market", "2.10", "2.00", "-4.76", "0.50", "2.00", "50", "Won"])
    output.seek(0)
    return StreamingResponse(output, media_type="text/csv",
                             headers={"Content-Disposition": "attachment; filename=bets.csv"})

# Allow running by calling: python main.py
if __name__ == "__main__":
    # run with uvicorn programmatically so "python main.py" works for you
    import uvicorn
    uvicorn.run("main:app", host="127.0.0.1", port=8000, reload=True)
