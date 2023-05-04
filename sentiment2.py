from transformers import AutoTokenizer, AutoModelForSequenceClassification, pipeline
import os
import glob
import pandas as pd

files = glob.glob(f'processed/*.csv')

def get_sentiment(text):
    model_name = 'siebert/sentiment-roberta-large-english'

    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModelForSequenceClassification.from_pretrained(model_name)

    classifier = pipeline('sentiment-analysis', model=model, tokenizer=tokenizer)

    sentiment_result = classifier(text)
    top_sentiment = max(sentiment_result, key=lambda x: x['score']) # Get the sentiment with the higher score
    polarity = 1 if top_sentiment['label'] == 'positive' else -1
    return top_sentiment['score'] * polarity

for file in files:
    df = pd.read_csv(file, index_col=None, header=0)

    df['Sentiment Score'] = df['Cleaned Comment'].apply(
        lambda x: get_sentiment(x))
    
    df['Adjusted Sentiment Score'] = df.apply(
        lambda x: x['Upvotes'] * x['Sentiment Score'], axis=1)
    
    df.to_csv(f'processed_new/{os.path.basename(file)}')