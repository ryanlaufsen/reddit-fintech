import requests
import os
from dotenv import load_dotenv

load_dotenv()

model = 'siebert/sentiment-roberta-large-english'
API_URL = f'https://api-inference.huggingface.co/models/{model}'
headers = {"Authorization": f"Bearer {os.environ['HUGGINGFACE_TOKEN']}"}

def analyze(data):
    payload = dict(inputs=data, options=dict(wait_for_model=True))
    response = requests.post(API_URL, headers=headers, json=payload)
    return response.json()

# Perform sentiment analysis using SiEBERT
def get_sentiment(text):
    try:
        sentiment_result = analyze(text)[0]
        top_sentiment = max(sentiment_result, key=lambda x: x['score']) # Get the sentiment with the higher score
        polarity = 1 if top_sentiment['label'] == 'positive' else -1
        return top_sentiment['score'] * polarity
    
    except Exception as e:
        print(e)