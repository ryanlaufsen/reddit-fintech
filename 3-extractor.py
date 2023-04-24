import pandas as pd
import reticker

nasdaq = pd.read_csv('data/nasdaq-listed-symbols_csv.csv')
nyse = pd.read_csv('data/nyse-listed-symbols_csv.csv')

tickers = pd.concat([nasdaq, nyse]).sort_values(by='Symbol')

extractor = reticker.TickerExtractor()
type(extractor.pattern)

def get_tickers(comment):
    mentioned_tickers = []

    for index, row in tickers.iterrows():
        for ticker in row.values:
            possible_tickers = extractor.extract(comment)
            if ticker in possible_tickers:
                mentioned_tickers.append(ticker)

    return mentioned_tickers


    
