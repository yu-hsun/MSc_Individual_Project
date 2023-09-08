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

for subreddit in ["China_irl"]: #search 'China_irl subreddit'
    sr = reddit.subreddit(subreddit)
    #search for the content related to apple products and services
    posts = sr.search('Apple OR 蘋果 OR 苹果 OR iphone OR mac OR vision pro OR ipad OR apple watch OR airpods OR appleTV OR ios OR apple music OR apple app store OR icloud', sort='new', time_filter='all', limit=None)  
    for submission in posts:
        submission.comment_sort = 'Top'
        submission.comments.replace_more(limit=0)
        comments = submission.comments.list()[:]

        #add content and time
        data['title'].append(submission.title)
        data['time'].append(datetime.fromtimestamp(submission.created_utc))

        #add submission context for each comment respectively
        for comment in comments:
            data['title'].append(submission.title + " " + comment.body) 
            data['time'].append(datetime.fromtimestamp(comment.created_utc)) 

df = pd.DataFrame(data)
df.to_csv('chinese_reddit.csv', index=False)
#print(df)