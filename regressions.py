import pandas as pd
import praw
from pushshift_py import PushshiftAPI as pi
from datetime import datetime, date, timedelta
import yfinance as yf
from stockstats import StockDataFrame
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.linear_model import Lasso
from sklearn.linear_model import Ridge


df = pd.read_csv("C:\\Users\\fcars\\Desktop\\FINA4320 NLP project\\for_regression_consolidated.csv")
#print(df)


#linear regresison
y = df['Actual Return']
X = df['Adjusted Sentiment Score'].values.reshape(-1,1)

X_train , X_test, y_train, y_test = train_test_split(X,y,test_size =  0.2, random_state = 42)

#get correlation of x and y
corr = df['Adjusted Sentiment Score'].corr(df['Actual Return'])
print("Correlation Coefficient:", corr)


linear_model = LinearRegression()
linear_model.fit(X_train,y_train)
linear_y_pred = linear_model.predict(X_test)
linear_mse = mean_squared_error(y_test,linear_y_pred)

print("Linear Regression Mean Squared Error:", linear_mse)


#lasso regression
lasso_model = Lasso(alpha=0.1)
lasso_model.fit(X_train, y_train)
lasso_y_pred = lasso_model.predict(X_test)

lasso_mse = mean_squared_error(y_test, lasso_y_pred)

print("Lasso Regression Mean Squared Error:", lasso_mse)

#Ridge Regression
ridge_model = Ridge(alpha=0.1)
ridge_model.fit(X_train, y_train)

ridge_y_pred = ridge_model.predict(X_test)

ridge_mse = mean_squared_error(y_test, ridge_y_pred)
print("Ridge Regression Mean Squared Error:", ridge_mse)


