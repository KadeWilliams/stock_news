from secrets import stock_api_key, news_api_key
import requests
import datetime as dt

now = dt.datetime.now()
month = now.month
year = now.year
day = now.day
weekday = now.weekday()

days = [day - 1 for day in range(now.day - 1, now.day + 1) if now.weekday() < 5]

STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

## STEP 1: Use https://www.alphavantage.co
# When STOCK price increase/decreases by 5% between yesterday and the day before yesterday then print("Get News").
stock_parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': stock_api_key
}

stock_endpoint = 'https://www.alphavantage.co/query?'
news_endpoint = 'https://newsapi.org/v2/everything?'

response = requests.get(stock_endpoint, params=stock_parameters)

stock_data = []

if month < 10:
    for day in days:
        stock_data.append(float(response.json()['Time Series (Daily)'][f'{year}-0{month}-{day}']['4. close']))
else:
    for day in days:
        stock_data.append(response.json()['Time Series (Daily)'][f'{year}-{month}-{day}'])

percentage_difference = (abs(stock_data[0] - stock_data[1]) / ((stock_data[0] + stock_data[1]) / 2)) * 100

news_parameters = {
    'q': COMPANY_NAME,
    'apiKey': news_api_key
}

titles = []
response = requests.get(news_endpoint, params=news_parameters)
for i in range(3):
    titles.append(response.json()['articles'][i]['title'])

if percentage_difference > 5:
    '\n'.join(titles)

## STEP 2: Use https://newsapi.org
# Instead of printing ("Get News"), actually get the first 3 news pieces for the COMPANY_NAME.

## STEP 3: Use https://www.twilio.com
# Send a seperate message with the percentage change and each article's title and description to your phone number. 


# Optional: Format the SMS message like this:
"""
TSLA: 🔺2%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
or
"TSLA: 🔻5%
Headline: Were Hedge Funds Right About Piling Into Tesla Inc. (TSLA)?. 
Brief: We at Insider Monkey have gone over 821 13F filings that hedge funds and prominent investors are required to file by the SEC The 13F filings show the funds' and investors' portfolio positions as of March 31st, near the height of the coronavirus market crash.
"""
