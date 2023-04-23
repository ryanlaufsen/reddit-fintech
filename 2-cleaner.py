import pandas as pd
import spacy
import en_core_web_sm
import re
import emoji
import praw
import nltk
import demoji
from nltk.tokenize import RegexpTokenizer
from praw.models import MoreComments
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer, PorterStemmer
from nltk import FreqDist
import datetime as dt
from datetime import datetime, timedelta
import string
from textblob import TextBlob
import spacy
from spacy import displacy

nlp = spacy.load('en_core_web_sm')
nltk.download('stopwords')
nltk.download('wordnet')

nlp = spacy.load('en_core_web_sm')


df = pd.read_csv('daily_discussion_moves.csv')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

#df.to_csv('sample.csv', index=False)


grouped_comments_df = df.groupby(by='Date').apply(lambda x:x)
#grouped_comments_df = grouped_comments_df.drop('Date',axis = 1)


def preprocess_text(text):
    # Remove emoji and gif
    text = re.sub(r'\\[a-zA-Z0-9]+', '', text)
    text = re.sub(r'\[\w+\]\(emote\|t5_\w+\|\d+\)', '', text)
    text = re.sub(r'\[\w+\]\(emote\|free_emotes_pack\|\w+\)', '', text)

    # Tokenize and clean string
    tokenizer = RegexpTokenizer('\w+|\$[\d\.]+|http\S+')
    tokenized_string = tokenizer.tokenize(text)

    # Convert tokens to lowercase
    lower_string_tokenized = [word.lower() for word in tokenized_string]

    # Remove stopwords
    all_stopwords = stopwords.words('english')
    tokens_without_sw = [word for word in lower_string_tokenized if not word in all_stopwords]

    # Lemmatize words
    lemmatizer = WordNetLemmatizer()
    lemmatized_tokens = ([lemmatizer.lemmatize(w) for w in tokens_without_sw])

    # Join cleaned tokens back into string
    cleaned_output = ' '.join(lemmatized_tokens)

    return cleaned_output

#Update the comment column with cleaned comment
grouped_comments_df['Cleaned Comment'] = grouped_comments_df['Comment'].apply(lambda x: preprocess_text(x))
#print((grouped_comments_df))

#Define a function to perform sentiment analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Apply sentiment analysis to 'Comment' column
grouped_comments_df['Sentiment_Score'] = grouped_comments_df['Cleaned Comment'].apply(lambda x: get_sentiment(x))
#grouped_comments_df.to_csv('sample.csv', index=False)
#print(grouped_comments_df)



import yfinance as yf
#import data of stock in NASQUE and NYSE
stock_df = pd.read_csv("C:\\Users\\fcars\\Desktop\\FINA4320 NLP project\\NYSE+NASDAQUE.csv")
#print(stock_df)
stocks_ticker = set(stock_df['Symbol'])

#print(stocks_ticker)
stock_entity = set(stock_df['Name'])
#print(type(grouped_comments_df['Cleaned Comment']))
#print(stock_entity)
#create a function to extract stock ticket or entity name

def extract_stock (text:str,directory):
    to_string = text.split()
    matches = []
    for word in to_string:
        if word.upper() in directory:
            matches.append(word.upper())
    return matches


directory = stocks_ticker
#grouped_comments_df.to_csv('sample.csv', index=False)
grouped_comments_df['Stock_Mentioned'] = grouped_comments_df['Cleaned Comment'].apply(lambda x:
                                                                                      extract_stock(x,directory))
grouped_comments_df.to_csv('sample.csv', index=False)



#generate stock return of next day given date and ticker
def get_next_day_return(ticker, date):
    # Convert the date string to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d').date()

    # Get the next day's date
    next_day = date + timedelta(days=1)

    # Get the stock data for the given ticker and date range
    stock_data = yf.download(ticker, start=date, end=next_day)

    # Calculate the daily return
    daily_return = (stock_data['Adj Close'][next_day] / stock_data['Adj Close'][date]) - 1

    # Return the daily return
    return daily_return




