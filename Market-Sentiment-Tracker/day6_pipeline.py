import pandas as pd
from sqlalchemy import create_engine
from sqlalchemy.engine import URL

print("--- Initializing Bulletproof Data Integration Pipeline ---")

# 1. Configuration
DB_USER = "root"
DB_PASS = "Bommineedi123"  # <-- Make sure to put your real password here!
DB_HOST = "localhost"
DB_NAME = "fintech_db"

connection_url = URL.create(
    "mysql+mysqlconnector",
    username=DB_USER,
    password=DB_PASS,
    host=DB_HOST,
    database=DB_NAME
)
engine = create_engine(connection_url)

# 2. Market Prices Pipeline
print("\n--- Processing Market Data ---")
try:
    # Read the CSV
    prices_df = pd.read_csv("market_prices.csv", header=0)
    
    # FORCE the dataframe to only use the first 8 columns (ignores Yahoo's weird formatting)
    prices_df = prices_df.iloc[:, :8]
    
    # FORCE the column names to perfectly match your MySQL Database
    prices_df.columns = ['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Asset']
    
    # Drop any rows that are entirely empty
    prices_df = prices_df.dropna(subset=['Date', 'Close'])
    
    print(f"Ready to insert {len(prices_df)} rows. Here is a sneak peek:")
    print(prices_df.head(2)) # Shows the first 2 rows in the terminal
    
    print("\nPushing to MySQL Database...")
    prices_df.to_sql(name='market_prices', con=engine, if_exists='append', index=False)
    print("Market Prices inserted successfully!")

except Exception as e:
    print(f"Error inserting market prices: {e}")

# 3. News Sentiment Pipeline
print("\n--- Processing Sentiment Data ---")
try:
    sentiment_df = pd.read_csv("news_sentiment_clean.csv")
    
    # FORCE column names for Sentiment
    sentiment_df.columns = ['Date', 'Asset', 'Headline', 'Sentiment_Score']
    sentiment_df = sentiment_df.dropna(subset=['Date', 'Sentiment_Score'])
    
    print(f"Ready to insert {len(sentiment_df)} rows.")
    sentiment_df.to_sql(name='news_sentiment', con=engine, if_exists='append', index=False)
    print("News Sentiment inserted successfully!")

except Exception as e:
    print(f"Error inserting sentiment data: {e}")

print("\n--- Pipeline Execution Complete ---")