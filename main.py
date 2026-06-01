from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import requests as rq
from os.path import dirname

app = FastAPI()
p = dirname(__file__)

templates = Jinja2Templates(directory=f"{p}/templates")
app.mount(f"/static", StaticFiles(directory=f"{p}/static"), name="static")

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    return templates.TemplateResponse("index.html", {"request": request})
@app.get("/crypto/{coin_id}")
async def get_crypto(coin_id: str):
    coin_url = f"https://api.coingecko.com/api/v3/coins/{coin_id.lower().strip()}"
    coin_response = rq.get(coin_url)

    if coin_response.status_code != 200:
        return JSONResponse(content={"error": f"Coin '{coin_id}' was not found!"}, status_code=404)
    coin_data = coin_response.json()

    chart_url = f"https://api.coingecko.com/api/v3/coins/{coin_id.strip().lower()}/market_chart"
    params = {"vs_currency": "usd", "days": "365", "interval": "daily"}

    chart_response = rq.get(chart_url, params=params)
    chart_data = chart_response.json()
    prices = chart_data["prices"]

    dates, closing_prices = [], []
    for i in prices:
        dates.append(i[0])
        closing_prices.append(i[1])
    
    return {
        "name": coin_data["name"],
        "symbol": coin_data["symbol"],
        "image": coin_data["image"]["large"],
        "current_price": coin_data["market_data"]["current_price"]["usd"],
        "market_cap": coin_data["market_data"]["market_cap"]["usd"],
        "high_24h": coin_data["market_data"]["high_24h"]["usd"],
        "low_24h": coin_data["market_data"]["low_24h"]["usd"],
        "price_change_24h": coin_data["market_data"]["price_change_percentage_24h"],
        "dates": dates,
        "prices": closing_prices
    }


# Command to start the app: uvicorn main:app --reload