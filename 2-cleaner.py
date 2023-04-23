import pandas as pd

df = pd.read_csv('data/daily_discussion_moves.csv')

# Convert post title into dates
df['Title'] = pd.to_datetime(df['Title'].str[30:])

print(df)