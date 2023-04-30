from datetime import datetime, timedelta
import yfinance as yf
import holidays

def next_two_business_days(date):
    next_day = date + timedelta(days=2)
    while next_day.weekday() in holidays.WEEKEND or next_day in holidays.US():
        next_day += timedelta(days=2)
    return next_day

def get_next_day_return(ticker, date):
    # Convert the date string to a datetime object
    date = datetime.strptime(date, '%Y-%m-%d').date()

    # Get the stock data for the given ticker and date range
    stock_data = yf.download(ticker,
                             start=date,
                             end=next_two_business_days(date),
                             period='5d',
                             progress=False,
                             ignore_tz=True,
                             repair=True)
    if stock_data.empty:
        return None
    
    # Calculate the daily return
    return (stock_data['Adj Close'][1] / stock_data['Adj Close'][0]) - 1
