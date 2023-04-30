import os
from dotenv import load_dotenv
import praw
from datetime import datetime
import csv

load_dotenv()

reddit = praw.Reddit(client_id=os.environ['REDDIT_CLIENT_ID'],
                     client_secret=os.environ['REDDIT_CLIENT_SECRET'],
                     user_agent='stock_sentimental_analysis')


subreddit = reddit.subreddit('wallstreetbets')

start_date = datetime(2023, 2, 27)
end_date = datetime(2023, 3, 31)

titles = []
authors = []
comments = []
upvotes = []

for submission in subreddit.search('flair_name:"Daily Discussion"', limit=None):
    if start_date <= datetime.fromtimestamp(submission.created_utc) <= end_date:
        if "What Are Your Moves" in submission.title:
            for comment in submission.comments:
                if isinstance(comment, praw.models.MoreComments):
                    continue

                titles.append(submission.title)
                authors.append(comment.author)
                comments.append(comment.body)
                upvotes.append(comment.score)
                
# Write data to CSV file
with open('../data/daily_discussion_moves.csv', 'w', encoding='utf-8', newline='') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['Title', 'Author', 'Comment', 'Upvotes'])
    for i in range(len(comments)):
        writer.writerow([titles[i], authors[i], comments[i], upvotes[i]])
