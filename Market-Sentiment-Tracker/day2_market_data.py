import yfinance as yf
import pandas as pd
import datetime

print("--- Initializing Market Data Fetcher (Fixed Version) ---")

assets = {
    "Gold": "GC=F",
    "Silver": "SI=F",
    "Nifty_50": "^NSEI"
}

end_date = datetime.date.today()
start_date = end_date - datetime.timedelta(days=2*365)
all_data = []

for name, ticker in assets.items():
    print(f"Downloading data for {name}...")
    df = yf.download(ticker, start=start_date, end=end_date)
    
    # 1. THE FIX: Flatten Yahoo's new double-header if it exists
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = df.columns.droplevel(1)
        
    df = df.reset_index()
    
    # 2. THE FIX: Ensure 'Adj Close' has an underscore for MySQL
    if 'Adj Close' in df.columns:
        df = df.rename(columns={'Adj Close': 'Adj_Close'})
    elif 'Close' in df.columns and 'Adj_Close' not in df.columns:
        df['Adj_Close'] = df['Close'] # Fallback
        
    df['Asset'] = name
    all_data.append(df)

print("Consolidating data into a single table...")
final_dataset = pd.concat(all_data, ignore_index=True)

# 3. THE FIX: Force the exact column order MySQL expects
final_dataset = final_dataset[['Date', 'Open', 'High', 'Low', 'Close', 'Adj_Close', 'Volume', 'Asset']]

filename = "market_prices.csv"
final_dataset.to_csv(filename, index=False)

print(f"Success! Clean data saved locally as '{filename}'")