import praw
from datetime import datetime
import pandas as pd

reddit = praw.Reddit(client_id='QzpLEbJDxX2PYJb9_43duw',
                     client_secret='31K5aLH4-nIwYitmIdFzIXqRW57LXw',
                     user_agent='stock_sentimental_analysis')


subreddit = reddit.subreddit('wallstreetbets')

start_date = datetime(2023, 4, 15)
end_date = datetime(2023, 4, 20)

titles = []
authors = []
comments = []


for submission in subreddit.search('flair_name:"Daily Discussion"', limit=None):
    if start_date <= datetime.fromtimestamp(submission.created_utc) <= end_date:
        if "What Are Your Moves" in submission.title:
            titles.append(submission.title)

            for comment in submission.comments:
                if isinstance(comment, praw.models.MoreComments):
                    continue

                authors.append(comment.author)
                comments.append(comment.body)

#print(authors)
#print(comments)

dict_of_dfs = {}
for i in range(len(titles)):
    df_user_comment = pd.DataFrame({'user_id': authors, 'comment': comments})
    dict_of_dfs[titles[i]] = df_user_comment

df = pd.concat(dict_of_dfs, axis=1)
df.to_csv('wallstreetbets_daily_moves_comments.csv', index=False)

print(df)





