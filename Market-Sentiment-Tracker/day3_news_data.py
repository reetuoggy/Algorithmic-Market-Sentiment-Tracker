import requests
import pandas as pd
import datetime

print("--- Initializing News Data Fetcher ---")

# 1. Your API Key Setup
# Replace with your actual NewsAPI key from Day 1
API_KEY = "6eb2044ad5174df08b852300c8dd972a"  
BASE_URL = "https://newsapi.org/v2/everything"

# 2. Define our topics and timeframe
topics = ["Gold", "Silver"]

# NewsAPI Developer Free Tier allows going back a maximum of 30 days
end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=29)

all_news = []

# 3. Loop through each topic and fetch the news
for topic in topics:
    print(f"Fetching news for {topic}...")
    
    # We build the URL parameters exactly how NewsAPI documentation requires
    params = {
        "q": topic,                      # The search keyword
        "from": start_date.strftime("%Y-%m-%d"), 
        "to": end_date.strftime("%Y-%m-%d"),
        "language": "en",                # English only
        "sortBy": "popularity",          # Get the most read articles
        "pageSize": 100,                 # Max articles per page on free tier
        "apiKey": API_KEY
    }
    
    response = requests.get(BASE_URL, params=params)
    data = response.json()
    
    # 4. Extract just the data we need (Date and Headline)
    if data.get("status") == "ok":
        articles = data["articles"]
        for article in articles:
            # Clean up the date string (e.g., "2026-05-15T08:00:00Z" -> "2026-05-15")
            raw_date = article["publishedAt"].split("T")[0] 
            
            all_news.append({
                "Date": raw_date,
                "Asset": topic,
                "Headline": article["title"]
            })
        print(f"Successfully retrieved {len(articles)} headlines for {topic}.")
    else:
        print(f"Error fetching {topic}: {data.get('message')}")

# 5. Consolidate and export to CSV
print("Formatting data...")
news_df = pd.DataFrame(all_news)

filename = "news_headlines_raw.csv"
news_df.to_csv(filename, index=False)
print(f"Success! Saved {len(news_df)} headlines locally as '{filename}'.")