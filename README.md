# reddit-fintech

Field project for HKU **FINA 4350 - Text Analytics and Natural Language Processing (NLP) in Finance and FinTech.**

(WIP) Our models determine whether r/wallstreetbets is an accurate predictor of daily price or volume movements, as compared to mainstream news sources. Furthermore, we use our results in pursuit of alpha.

## Setup
> You need the following values in an .env file:
> - `REDDIT_CLIENT_ID` 
> - `REDDIT_CLIENT_SECRET`
> - HUGGINGFACE_TOKEN

Please note: data must be placed in the "processed" directory!

## Scraping data from Reddit
```
python3 1-scraper.py
```
The output file will be in `data/daily_discussion_moves.csv`

## Running the model
```
pip install -r requirements.txt
python3 main.py
```