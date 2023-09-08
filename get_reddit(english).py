import praw
import pandas as pd
from datetime import datetime

reddit = praw.Reddit(
    client_id="my client id here",
    client_secret="my client secret here",
    user_agent="my user agent here",
)

data = {
    'title': [],
    'time': [],
}

for submission in reddit.subreddit('apple').new(limit=None): #search 'apple subreddit'
    submission.comment_sort = 'Top'
    submission.comments.replace_more(limit=0)
    comments = submission.comments.list()[:] #get all comments for every submission

    #add content and time
    data['title'].append(submission.title)
    data['time'].append(datetime.fromtimestamp(submission.created_utc))

    #add submission context for each comment respectively
    for comment in comments:
        data['title'].append(submission.title + " " + comment.body)  
        data['time'].append(datetime.fromtimestamp(comment.created_utc))  

df = pd.DataFrame(data)
df.to_csv('english_reddit.csv', index=False)
#print(df)
