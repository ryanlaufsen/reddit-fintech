import pandas as pd
import re
from nltk.tokenize import RegexpTokenizer
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

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