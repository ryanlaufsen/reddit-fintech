import pandas as pd
import importlib
cleaner = importlib.import_module('2-cleaner')
extractor = importlib.import_module('3-extractor')
analyzer = importlib.import_module('4-analyzer')
calc = importlib.import_module('5-calculator')

df = pd.read_csv('data/daily_discussion_moves.csv').tail(5)

# Extract stock tickers from raw comments
df['Tickers'] = df['Comment'].apply(
    lambda x: extractor.get_tickers(x))

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

# Update the comment column with cleaned comment
df['Cleaned Comment'] = df['Comment'].apply(
    lambda x: cleaner.preprocess_text(x))

# Apply sentiment analysis to 'Comment' column
df['Sentiment Score'] = df['Cleaned Comment'].apply(
    lambda x: analyzer.get_sentiment(x))

# Calculate actual daily returns
df = df[df['Tickers'].map(lambda d: len(d)) > 0]  # Remove rows with no ticker mentions

# Convert datetime to string
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

df['Actual Return'] = df.apply(
    lambda x: calc.get_next_day_return(x['Tickers'], x['Date']), axis=1)

print(df[['Comment', 'Tickers', 'Sentiment Score', 'Actual Return', 'Date']])
