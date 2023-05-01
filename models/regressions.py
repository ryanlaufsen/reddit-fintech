import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression, Lasso, Ridge, LogisticRegression


def train_and_test(X, y, size, state):
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=size, random_state=state)
    
    return X_train, X_test, y_train, y_test


def linear_reg(X_train, X_test, y_train, y_test):
    model = LinearRegression()
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r_sq = model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)

    return {
        'mse': mse,
        'r_sq': r_sq
    }

def lasso_reg(X_train, X_test, y_train, y_test, a):
    model = Lasso(alpha=a)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r_sq = model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)

    return {
        'mse': mse,
        'r_sq': r_sq
    }

def ridge_reg(X_train, X_test, y_train, y_test, a):
    model = Ridge(alpha=a)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    r_sq = model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)

    return {
        'mse': mse,
        'r_sq': r_sq
    }

def logistic_reg(X_train, X_test, y_train, y_test):
    model = LogisticRegression(multi_class='ovr')
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    accuracy = model.score(X_test, y_test)
    mse = mean_squared_error(y_test, y_pred)

    return {
        'mse': mse,
        'accuracy': accuracy
    }
