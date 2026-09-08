# Algorithmic Market Sentiment Tracker 

## Overview
Designed and deployed an end-to-end ETL data pipeline to analyze the correlation between financial news sentiment and asset price volatility. This project acts as an automated risk-alert engine, scraping unstructured text, scoring emotional polarity, and merging it with historical market data to flag critical market movements.

## Tech Stack
* **Languages:** Python (Pandas, BeautifulSoup, VADER NLP), Advanced SQL (MySQL)
* **Architecture:** Database routing via `sqlalchemy`, API extraction via `yfinance`
* **Business Intelligence:** Power BI, DAX (Data Analysis Expressions)

## System Architecture
1. **Extraction:** Python scraper bypasses anti-bot headers to pull daily financial news, while querying Yahoo Finance APIs for rolling 2-year historical asset prices (Gold, Silver, Nifty_50).
2. **Transformation:** NLP VADER model quantifies text sentiment into mathematical compound scores. Pandas flattens API MultiIndex arrays and normalizes schemas.
3. **Loading & Modeling:** Data is loaded into a local MySQL database. Advanced SQL (CTEs, Window Functions, LEFT JOINS) constructs a production-ready View aligning daily sentiment averages with market closing prices.
4. **Visualization & Logic:** Power BI connects directly to MySQL. A custom DAX risk engine calculates day-over-day price drops against sentiment thresholds to autonomously generate `CRITICAL WARNING` or `MARKET NOISE` signals.

## Future Product Roadmap
* **NLP Upgrade:** Transitioning from the generalized VADER model to **FinBERT**, a model specifically trained on financial texts, to resolve false-neutral misclassifications of positive financial restructuring terminology.
