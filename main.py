import pandas as pd
import importlib
cleaner = importlib.import_module('2-cleaner')
extractor = importlib.import_module('3-extractor')
analyzer = importlib.import_module('4-analyzer')

df = pd.read_csv('data/daily_discussion_moves.csv')

# Extract stock tickers from raw comments
df['Tickers'] = None

for index, row in df.tail(5).iterrows():
    df.at[index, 'Tickers'] = extractor.get_tickers(row['Comment'])

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

grouped_comments_df = df.groupby(by='Date').apply(lambda x: x)
grouped_comments_df = grouped_comments_df.drop('Date', axis=1)

# Update the comment column with cleaned comment
grouped_comments_df['Cleaned Comment'] = grouped_comments_df['Comment'].apply(
    lambda x: cleaner.preprocess_text(x))

# Apply sentiment analysis to 'Comment' column
grouped_comments_df['Sentiment Score'] = grouped_comments_df['Cleaned Comment'].apply(
    lambda x: analyzer.get_sentiment(x))
print(grouped_comments_df[['Comment', 'Tickers', 'Sentiment Score']])

