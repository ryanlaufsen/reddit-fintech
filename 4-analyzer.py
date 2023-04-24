import pandas as pd
import nltk
from textblob import TextBlob
import importlib
cleaner = importlib.import_module('2-cleaner')

for resource in ['corpora/stopwords', 'corpora/wordnet']:
    try:
        nltk.find(resource)
    except LookupError:
        nltk.download(resource)

# Define a function to perform sentiment analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity


df = pd.read_csv('data/daily_discussion_moves.csv')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

grouped_comments_df = df.groupby(by='Date').apply(lambda x: x)
grouped_comments_df = grouped_comments_df.drop('Date', axis=1)

# Update the comment column with cleaned comment
grouped_comments_df['Cleaned Comment'] = grouped_comments_df['Comment'].apply(lambda x: cleaner.preprocess_text(x))

# Apply sentiment analysis to 'Comment' column
grouped_comments_df['Sentiment_Score'] = grouped_comments_df['Cleaned Comment'].apply(
    lambda x: get_sentiment(x))
print(grouped_comments_df.head(5))
