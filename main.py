import requests
from twilio.rest import Client
import os
from dotenv import load_dotenv

STOCK_NAMES = ["RCKT", "SONY", "SWPPX"]
COMPANY_NAME = "Rocket Pharmaceuticals Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

load_dotenv()
VIRTUAL_TWILIO_NUMBER = os.getenv('VIRTUAL_TWILIO_NUMBER')
VERIFIED_NUMBER = os.getenv('VERIFIED_NUMBER')

STOCK_API_KEY = os.getenv('STOCK_API_KEY')
NEWS_API_KEY = os.getenv('NEWS_API_KEY')
TWILIO_SID = os.getenv('TWILIO_SID')
TWILIO_AUTH_TOKEN = os.getenv('TWILIO_AUTH_TOKEN')

responses = [];
for x in STOCK_NAMES:
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": x,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)

    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]
    print('yesterdays closing price: ', yesterday_closing_price)

    day_before_yesterday_data = data_list[1]
    day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
    print('2 days ago closing price:', day_before_yesterday_closing_price)

    difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
    up_down = None
    if difference > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    diff_percent = round((difference / float(yesterday_closing_price)) * 100)
    print('price difference: ',diff_percent)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    text_message =  [f"{x}: {up_down}{diff_percent}%\nyesterday: {yesterday_closing_price}\nday before yesterday: {day_before_yesterday_closing_price}"]
    message = client.messages.create(
        body=text_message,
        from_=VIRTUAL_TWILIO_NUMBER,
        to=VERIFIED_NUMBER
    )

