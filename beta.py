import pandas as pd
import praw
import re

reddit = praw.Reddit(client_id='QzpLEbJDxX2PYJb9_43duw',
                     client_secret='31K5aLH4-nIwYitmIdFzIXqRW57LXw',
                     user_agent='stock_sentimental_analysis')

#scrape reddit comments
titles = []
ids = []
author = []
comments = []

for submission in reddit.subreddit('wallstreetbets').hot(limit=1):
    titles.append(submission.title)
    ids.append(submission.id)

    for comment in submission.comments:
        if isinstance(comment, praw.models.MoreComments):
            continue

        author.append(comment.author)
        comments.append(comment.body)

# extract stock mentions from comments
stocks = ['AAPL', 'GOOGL', 'TSLA', 'AMZN']  # list of stock symbols/names
pattern = '|'.join(stocks)  # regex pattern for matching stock mentions
mentions = []
for comment in comments:
    mention = re.findall(pattern, comment, re.IGNORECASE)  # find stock mentions using regex
    mentions.append(mention)

dict_of_dfs = {}
for i in range(len(titles)):
    df_user_comment = pd.DataFrame({'user_id': author, 'comment': comments, 'stock_mention': mentions})
    dict_of_dfs[titles[i]] = df_user_comment

df = pd.concat(dict_of_dfs, axis=1)
print(df)
