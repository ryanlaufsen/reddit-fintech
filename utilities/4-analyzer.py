import pandas as pd
import nltk
from textblob import TextBlob

for resource in ['corpora/stopwords', 'corpora/wordnet']:
    try:
        nltk.find(resource)
    except LookupError:
        nltk.download(resource)

# Define a function to perform sentiment analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity
