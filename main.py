import requests
from twilio.rest import Client

VIRTUAL_TWILIO_NUMBER = '+18669543817'
VERIFIED_NUMBER = '+19258900267'

STOCK_NAMES = ["RCKT", "SONY"]
STOCK_NAME = "RCKT"
COMPANY_NAME = "Rocket Pharmaceuticals Inc"

STOCK_ENDPOINT = "https://www.alphavantage.co/query"
NEWS_ENDPOINT = "https://newsapi.org/v2/everything"

STOCK_API_KEY = "3O4WIGPYP879GH3F"
NEWS_API_KEY = "433f8287c1b8476784b6953ccff0f06d"
TWILIO_SID = 'AC78e617c34d0ca181b54d4abe0834115c'
TWILIO_AUTH_TOKEN = 'df3da7cae679d0a51ab9314e1348bc8a'

## STEP 1: Use https://www.alphavantage.co/documentation/#daily
# When stock price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").

#Get yesterday's closing stock price
stock_params = {
    "function": "TIME_SERIES_DAILY",
    "symbol": STOCK_NAME,
    "apikey": STOCK_API_KEY,
}


responses = [];
for x in STOCK_NAMES:
    stock_params = {
        "function": "TIME_SERIES_DAILY",
        "symbol": x,
        "apikey": STOCK_API_KEY,
    }
    response = requests.get(STOCK_ENDPOINT, params=stock_params)
    # print('scotttest response', response.json())
    # responses.append(response.json())

# print('scotttest responses',responses)
# response = requests.get(STOCK_ENDPOINT, params=stock_params)
    data = response.json()["Time Series (Daily)"]
    data_list = [value for (key, value) in data.items()]
    yesterday_data = data_list[0]
    yesterday_closing_price = yesterday_data["4. close"]
    print('yesterdays closing price: ', yesterday_closing_price)

    #Get the day before yesterday's closing stock price
    day_before_yesterday_data = data_list[1]
    day_before_yesterday_closing_price = day_before_yesterday_data["4. close"]
    print('2 days ago closing price:', day_before_yesterday_closing_price)

    #Find the positive difference between 1 and 2. e.g. 40 - 20 = -20, but the positive difference is 20. Hint: https://www.w3schools.com/python/ref_func_abs.asp
    difference = float(yesterday_closing_price) - float(day_before_yesterday_closing_price)
    up_down = None
    if difference > 0:
        up_down = "🔺"
    else:
        up_down = "🔻"

    #Work out the percentage difference in price between closing price yesterday and closing price the day before yesterday.
    diff_percent = round((difference / float(yesterday_closing_price)) * 100)
    print('price difference: ',diff_percent)
    client = Client(TWILIO_SID, TWILIO_AUTH_TOKEN)
    text_message =  [f"{x}: {up_down}{diff_percent}%\nyesterday: {yesterday_closing_price}\nday before yesterday: {day_before_yesterday_closing_price}"]
    message = client.messages.create(
        body=text_message,
        from_=VIRTUAL_TWILIO_NUMBER,
        to=VERIFIED_NUMBER
    )

