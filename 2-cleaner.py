import pandas as pd
import re
import nltk
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from textblob import TextBlob


nltk.download('stopwords')
nltk.download('wordnet')

df = pd.read_csv('data/daily_discussion_moves.csv')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

grouped_comments_df = df.groupby(by='Date').apply(lambda x:x)
grouped_comments_df = grouped_comments_df.drop('Date',axis = 1)


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

# Update the comment column with cleaned comment
grouped_comments_df['Cleaned Comment'] = grouped_comments_df['Comment'].apply(lambda x: preprocess_text(x))

# Define a function to perform sentiment analysis using TextBlob
def get_sentiment(text):
    blob = TextBlob(text)
    return blob.sentiment.polarity

# Apply sentiment analysis to 'Comment' column
grouped_comments_df['Sentiment_Score'] = grouped_comments_df['Cleaned Comment'].apply(lambda x: get_sentiment(x))
print(grouped_comments_df)