# IMPORTS
from secrets import stock_api_key, news_api_key, twilio_creditials
import requests
from twilio.rest import Client

# # CONSTANTS
STOCK = "TSLA"
COMPANY_NAME = "Tesla Inc"

stock_parameters = {
    'function': 'TIME_SERIES_DAILY_ADJUSTED',
    'symbol': STOCK,
    'apikey': stock_api_key
}

stock_endpoint = 'https://www.alphavantage.co/query?'

# STOCK DATA AND MANIPULATION
response = requests.get(stock_endpoint, params=stock_parameters)
data = response.json()['Time Series (Daily)']
data_list = [value for (key, value) in data.items()]
past_two_days = [data_list[0], data_list[1]]
closing_prices = [float(past_two_days[0]['4. close']), float(past_two_days[1]['4. close'])]

percentage_difference = (abs(closing_prices[0] - closing_prices[1]) / ((closing_prices[0] + closing_prices[1]) / 2)) * 100

up_down = '🔺'

if closing_prices[1] > closing_prices[0]:
    percentage_difference *= -1
    up_down = '🔻'

#
# # NEWS DATA AND MANIPULATION
news_parameters = {
    'qInTitle': COMPANY_NAME,
    'apiKey': news_api_key
}

news_endpoint = 'https://newsapi.org/v2/everything?'

story = []
response = requests.get(news_endpoint, params=news_parameters)
articles = response.json()['articles'][:3]

# # TWILIO MESSAGE AND OUTPUT
formatted_articles = [f"Headline: {article['title']}\n\nBrief: {article['description']}" for article in articles]
if abs(percentage_difference) > 5:
    for article in formatted_articles:
        client = Client(twilio_creditials['account_sid'], twilio_creditials['auth_token'])

        message = client.messages \
            .create(
            body=f"{STOCK}: {up_down}{int(percentage_difference)}%\n\n{article}",
            from_=twilio_creditials['phone'],
            to=twilio_creditials['my_phone']
        )

    print(message.status)
