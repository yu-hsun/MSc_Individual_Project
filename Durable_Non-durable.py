import pandas as pd

df = pd.read_csv('english_reddit_scores.csv')

#filter durable and != durable then = non-durable
df_filtered = df[df['title'].str.contains('iPhone|Mac|iPad|AppleTV|Studio Display|Pro Display XDR')]#durable
unfiltered_df = df[~df['title'].str.contains('iPhone|Mac|iPad|AppleTV|Studio Display|Pro Display XDR')]#non-durable

import datetime
import numpy as np

df = df_filtered #or unfiltered_df
df['time']=pd.to_datetime(df['time'])

#count compound mean score for each day
i = 0
mean_lst = [] #mean of each day's comp    
y = datetime.datetime.now()-datetime.timedelta(days=i)
sd = datetime.datetime(y.year, y.month, y.day, 0, 0, 0)
ed = datetime.datetime(y.year, y.month, y.day, 23, 59, 59)
while sd>=np.min(df['time']): #compare the date to the earliest date of all reddits that have been captured
    y = datetime.datetime.now()-datetime.timedelta(days=i) #separate each day
    sd = datetime.datetime(y.year, y.month, y.day, 0, 0, 0)
    ed = datetime.datetime(y.year, y.month, y.day, 23, 59, 59)
    a = np.mean(df[(sd <= df['time']) & (df['time'] <= ed)]['pos'])
    b = np.mean(df[(sd <= df['time']) & (df['time'] <= ed)]['neg'])
    c = ((a-b)+1)/2
    mean_lst.append(c)
    i+=1

mean_lst = [x for x in mean_lst if not np.isnan(x)]    
daylst = pd.to_datetime(df['time']).dt.date.unique().tolist()
mean_lst.reverse()
daylst.reverse()

data = {'Date':daylst, 'Mean':mean_lst}
df = pd.DataFrame(data)
df.to_csv('durable_mean.csv', index=False) # non_durable_mean
