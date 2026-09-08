import yfinance as yf
import requests

print("--- Testing Setup ---")

# 1. Fetch Gold Price
gold = yf.Ticker("GC=F")
price = gold.history(period="1d")['Close'].iloc[0]
print(f"Success! Current Gold Price is: ${price:.2f}")

# 2. Fetch Latest News
# VERY IMPORTANT: Replace the text below with your actual NewsAPI key
API_KEY = "6eb2044ad5174df08b852300c8dd972a" 

url = f"https://newsapi.org/v2/everything?q=finance&apiKey={API_KEY}&pageSize=1"
news_data = requests.get(url).json()
headline = news_data['articles'][0]['title']
print(f"Success! Latest Finance Headline: '{headline}'")