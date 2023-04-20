import pandas as pd
import praw

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

dict_of_dfs = {}
for i in range(len(titles)):
    df_user_comment = pd.DataFrame({'user_id': author, 'comment': comments})
    dict_of_dfs[titles[i]] = df_user_comment

df = pd.concat(dict_of_dfs, axis=1)
print(df)