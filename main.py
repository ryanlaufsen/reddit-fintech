import numpy as np
import pandas as pd
import importlib
cleaner = importlib.import_module('2-cleaner')
extractor = importlib.import_module('3-extractor')
analyzer = importlib.import_module('4-analyzer')
calc = importlib.import_module('5-calculator')
import csv
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression

df = pd.read_csv('data/daily_discussion_moves.csv')

#df = df.head(n=1000)

# Extract stock tickers from raw comments
df['Ticker'] = df['Comment'].apply(
    lambda x: extractor.get_tickers(x))
df = df.explode('Ticker')

# Convert post title into dates
df['Date'] = pd.to_datetime(df['Title'].str[30:])

df = df.sort_values(by='Date', ascending=False)

# Update the comment column with cleaned comment
df['Cleaned Comment'] = df['Comment'].apply(
    lambda x: cleaner.preprocess_text(x))

# Apply sentiment analysis to 'Comment' column
df['Sentiment Score'] = df['Cleaned Comment'].apply(
    lambda x: analyzer.get_sentiment(x))

# Multiply sentiment by upvotes
df['Adjusted Sentiment Score'] = df.apply(
    lambda x: x['Upvotes'] * x['Sentiment Score'], axis=1)

# Sum sentiment, grouping by ticker and date
df.groupby(['Ticker', 'Date']).agg({'Adjusted Sentiment Score': 'sum'})

# Calculate actual daily returns
df = df[df['Ticker'].notnull()]  # Remove rows with no ticker mentions

# Convert datetime to string
df['Date'] = df['Date'].dt.strftime('%Y-%m-%d')

df['Actual Return'] = df.apply(
    lambda x: calc.get_next_day_return(x['Ticker'], x['Date']), axis=1)

#print(df[['Ticker', 'Adjusted Sentiment Score', 'Actual Return', 'Date']])

y = df['Actual Return']

X = df['Adjusted Sentiment Score']
X_train , X_test, y_train, y_test = train_test_split(X,y,test_size =  0.2, random_state = 42)

model = LinearRegression()
model.fit(X_train,y_train)
#
y_pred = model.predict(X_test)
#
mse = mean_squared_error(y_test, y_pred)
rmse = np.sqrt(mse)
r_squared = model.score(X_test, y_test)
print("Root Mean Squared Error:", rmse)
print("R-squared:", r_squared)
