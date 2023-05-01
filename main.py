import pandas as pd
import os
import glob
import importlib
datawriter = importlib.import_module('utilities.datawriter')
regressions = importlib.import_module('models.regressions')

# Configure directory names for data download, processed files, and final results
config_dirs = {
    'data': 'data',
    'processed': 'processed',
    'results': 'results'
}

# # Create aforementioned directories
# for dir in config_dirs:
#     if not os.path.exists(dir):
#         os.makedirs(dir)
#         print(f'Created /{dir} directory.')

# # Pause / resume controls. Parameters can be edited depending on hardware / network capabilities
# f = f'{config_dirs["data"]}/daily_discussion_moves.csv'
# start_index = 0
# chunk_size = 100

# for i in range(start_index, len(pd.read_csv(f)), chunk_size):
#     df_part = datawriter.write(i, chunk_size, f)
#     if not df_part.empty:
#         df_part.to_csv(f'{config_dirs["processed"]}/processed_{i}_{i + chunk_size}.csv')
#         print(f'Processed and saved rows {i} to {i + chunk_size}.'
#               f'({len(df_part)} {"tickers" if len(df_part) > 1 else "ticker"} found.)'
#               )

# Concatenate processed data and perform additional pre-processing
df = datawriter.consolidate(glob.glob(f'{config_dirs["processed"]}/*.csv'))
df = df.sort_values(by=['Date'])
df = df[['Title', 'Date', 'Comment', 'Adjusted Sentiment Score', 'Actual Return']] # ['Comment'] is only kept here for de-duplicating purposes
df = df.drop_duplicates(keep='first')

reg_df = df[['Adjusted Sentiment Score', 'Actual Return']]
reg_df = reg_df.dropna()

corr = reg_df['Adjusted Sentiment Score'].corr(reg_df['Actual Return'])

# Train on 80% of the data, test on remaining 20%
X_train, X_test, y_train, y_test = regressions.train_and_test(reg_df, 0.2, 42) # Random state is set to an int for reproducible results

linear_regression = regressions.linear_reg(X_train, X_test, y_train, y_test)
lasso_regression = regressions.lasso_reg(X_train, X_test, y_train, y_test)
ridge_regression = regressions.ridge_reg(X_train, X_test, y_train, y_test)

print("Correlation Coefficient:", corr)
print("Linear Regression:", linear_regression)
print("Lasso Regression:", lasso_regression)
print("Ridge Regression:", ridge_regression)
