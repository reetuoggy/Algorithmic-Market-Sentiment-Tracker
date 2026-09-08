import pandas as pd
from vaderSentiment.vaderSentiment import SentimentIntensityAnalyzer

print("--- Initializing Sentiment NLP Engine ---")

# 1. Load the raw news data we fetched on Day 3
try:
    df = pd.read_csv("news_headlines_raw.csv")
    print(f"Successfully loaded {len(df)} headlines.")
except FileNotFoundError:
    print("Error: 'news_headlines_raw.csv' not found. Make sure you ran Day 3's script successfully.")
    exit()

# 2. Initialize VADER Sentiment Analyzer
analyzer = SentimentIntensityAnalyzer()

# 3. Create a function to extract the compound sentiment score
def get_sentiment_score(headline):
    # VADER analyzes the text and returns a dictionary of scores (pos, neu, neg, compound)
    scores = analyzer.polarity_scores(str(headline))
    return scores['compound'] # Compound is the overall score from -1 to +1

print("Analyzing headlines (this will take just a few seconds)...")

# 4. Apply the scoring function to every row in our Headline column
df['Sentiment_Score'] = df['Headline'].apply(get_sentiment_score)

# 5. Save the newly scored data to a clean CSV file
output_filename = "news_sentiment_clean.csv"
df.to_csv(output_filename, index=False)

print(f"Success! Scored dataset saved as '{output_filename}'")

# Quick sneak peek of the results in the terminal
print("\n--- Sample Results ---")
print(df[['Headline', 'Sentiment_Score']].head())