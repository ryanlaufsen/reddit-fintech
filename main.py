import pandas as pd
import importlib
cleaner = importlib.import_module('2-cleaner')
extractor = importlib.import_module('3-extractor')
analyzer = importlib.import_module('4-analyzer')
calc = importlib.import_module('5-calculator')

df = pd.read_csv('data/daily_discussion_moves.csv').tail(5)

# Extract stock tickers from raw comments
df['Ticker'] = df['Comment'].apply(
    lambda x: extractor.get_tickers(x))
df = df.explode('Ticker')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

# Update the comment column with cleaned comment
df['Cleaned Comment'] = df['Comment'].apply(
    lambda x: cleaner.preprocess_text(x))

# Apply sentiment analysis to 'Comment' column
df['Sentiment Score'] = df['Cleaned Comment'].apply(
    lambda x: analyzer.get_sentiment(x))

# Sum sentiment, grouping by ticker and date
df.groupby(['Ticker', 'Date']).agg({'Sentiment Score': 'sum'})

# Calculate actual daily returns
df = df[df['Ticker'].notnull()]  # Remove rows with no ticker mentions
# Convert datetime to string
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

df['Actual Return'] = df.apply(
    lambda x: calc.get_next_day_return(x['Ticker'], x['Date']), axis=1)

print(df[['Ticker', 'Sentiment Score', 'Actual Return', 'Date']])
