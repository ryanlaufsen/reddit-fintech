import pandas as pd
import importlib
cleaner = importlib.import_module('utilities.2-cleaner')
extractor = importlib.import_module('utilities.3-extractor')
analyzer = importlib.import_module('utilities.4-analyzer')
calc = importlib.import_module('utilities.5-calculator')

def write(start_index, chunk_size, f):
    df = pd.read_csv(f,
                    skiprows=None if start_index == 0 else range(1,start_index+1),
                    nrows=chunk_size,
                    on_bad_lines='warn').head(1)

    # Extract stock tickers from raw comments
    df['Ticker'] = df['Comment'].apply(
        lambda x: extractor.get_tickers(x))
    df = df.explode('Ticker')

    # Calculate actual daily returns
    df = df[df['Ticker'].notnull()]  # Remove rows with no ticker mentions
    if df.empty:
        return

    # Convert post title into dates
    df['Date'] = pd.to_datetime(df['Title'].str[30:])

    df = df.sort_values(by='Date', ascending=True)

    # Add cleaned comment column
    df['Cleaned Comment'] = df['Comment'].apply(
        lambda x: cleaner.preprocess_text(x))

    # Apply sentiment analysis to cleaned comments
    df['Sentiment Score'] = df['Cleaned Comment'].apply(
        lambda x: analyzer.get_sentiment(x))

    # Multiply sentiment by upvotes
    df['Adjusted Sentiment Score'] = df.apply(
        lambda x: x['Upvotes'] * x['Sentiment Score'], axis=1)

    # Convert datetime to string
    df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

    df['Actual Return'] = df.apply(
        lambda x: calc.get_next_day_return(x['Ticker'], x['Date']), axis=1)

    end_index = start_index + chunk_size - 1
    if end_index > len(df):
        end_index = len(df)

    df.to_csv(f'for_regression/for_regression_{start_index}_{end_index}.csv')

def consolidate(files):
    '''
    Consolidates files generated with datawriter.write() by continuously appending into one large dataframe.
    Returns a pandas dataframe.
    '''

    df_list = []

    for file in files:
        df = pd.read_csv(file, index_col=None, header=0)
        df_list.append(df)

    return pd.concat(df_list, axis=0, ignore_index=True)