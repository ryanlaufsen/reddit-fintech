from datetime import datetime, timedelta
import yfinance as yf

def get_next_day_return(ticker, date):
    # Convert the date string to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d').date()

    # Get the next day's date
    next_day = date + timedelta(days=2)

    # Get the stock data for the given ticker and date range
    stock_data = yf.download(ticker, start=date, end=next_day, progress=False)

    # Calculate the daily return
    daily_return = (stock_data['Adj Close'][1] / stock_data['Adj Close'][0]) - 1

    # Return the daily return
    return daily_return
