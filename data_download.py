import requests

# Set up initial parameters
base_url = "https://api.pushshift.io/reddit/search/submission/"
subreddit = "wallstreetbets"
title_string = "What Are Your Moves Tomorrow"
start_time = 1583539200  # epoch time for 7 Mar 2020 00:00:00 GMT
end_time = 1586217600  # epoch time for 7 Apr 2020 00:00:00 GMT
params = {"subreddit": subreddit, "title": title_string, "after": start_time, "before": end_time, "size": 1000}

# Loop until all submission ids are retrieved
ids = []
submissions = []

while True:
    response = requests.get(base_url, params=params)
    if response.status_code != 200:
        print("Error:", response.status_code)
        break
    data = response.json()["data"]
    submissions.append(data)
    if len(data) == 0:
        break
    for submission in data:
        ids.append(submission["id"])
    params["after"] = data[-1]["created_utc"]

# Return ids in a list
print(ids)
