import pandas as pd
import importlib
cleaner = importlib.import_module('2-cleaner')
extractor = importlib.import_module('3-extractor')
analyzer = importlib.import_module('4-analyzer')
calc = importlib.import_module('5-calculator')

df = pd.read_csv('data/daily_discussion_moves.csv').sample(n=20)

# Extract stock tickers from raw comments
df['Ticker'] = df['Comment'].apply(
    lambda x: extractor.get_tickers(x))
df = df.explode('Ticker')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=True)

# Update the comment column with cleaned comment
df['Cleaned Comment'] = df['Comment'].apply(
    lambda x: cleaner.preprocess_text(x))

# Apply sentiment analysis to 'Comment' column
df['Sentiment Score'] = df['Cleaned Comment'].apply(
    lambda x: analyzer.get_sentiment(x))

# Multiply sentiment by upvotes
df['Adjusted Sentiment Score'] = df.apply(
    lambda x: x['Upvotes'] * x['Sentiment Score'], axis=1)

# Calculate actual daily returns
df = df[df['Ticker'].notnull()]  # Remove rows with no ticker mentions

# Convert datetime to string
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

df['Actual Return'] = df.apply(
    lambda x: calc.get_next_day_return(x['Ticker'], x['Date']), axis=1)

# Sum sentiment, grouping by ticker and date
df = df.groupby(['Ticker', 'Date']).agg({'Adjusted Sentiment Score': 'sum', 'Actual Return': 'mean'})

print(df[['Ticker', 'Adjusted Sentiment Score', 'Actual Return', 'Date']])

# df.to_csv('data/for_regression.csv')
