# MSc_Individual_Project
## Consumer Sentiment towards Various Apple Products in Different Regions and its Impact on Apple’s Stock Price

- Performed sentiment analysis on Reddit comments towards Apple products using NLP models to examine correlations with Apple stock prices; project involved large-scale data collection, preprocessing, time series analysis, and regression techniques.
- This project consists of several Python scripts and CSV files to analyze sentiment data from Reddit comments in both English and Chinese regarding Apple products. It calculates daily compound sentiment scores and investigates their correlation with Apple's stock price. Here's an overview of the files and their functionality:

## Python Files

1. **get_reddit(chinese).py**: Collects Chinese Reddit data regarding Apple products.
2. **get_reddit(english).py**: Collects English Reddit data regarding Apple products.
3. **MacBERT.py**: Calculates the sentiment scores for the Chinese Reddit data.
4. **CardiffNLP.py**: Calculates the sentiment scores for the English Reddit data.
5. **Durable_Non-durable.py**: Returns daily compound scores for durable and non-durable goods.
6. **Product-Specific.py**: Classifies Reddit content by product and calculates product-specific scores.
7. **Region-Specific.py**: Calculates region-specific scores.
8. **Granger.py**: Conducts Granger causality tests using daily compound scores and AAPL.csv.
9. **DC_LE_backtest.py**: Generates DC points and local extremes and conducts backtests for trading strategies.
