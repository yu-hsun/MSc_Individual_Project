import pandas as pd
df = pd.read_csv('english_reddit_scores.csv')
per = {'per':0}
x = []
data = {'per':x}

#5 product categories
data1 = {'iphone':x,'ipad':x,'services':x,'mac':x,'wearables & home accessories':x}
data2 = {'compound':x}
per = pd.DataFrame(data)
df1 = pd.DataFrame(data1)
df2 = pd.DataFrame(data2)
df = pd.concat([df,per,df2,df1], axis=1)

#search for the related content and give the revenue percentage
#a context can have more then one categories be mentioned
for i in range(len(df)):
    if 'iphone' in df.iloc[i, 0].lower():
        df.iloc[i, 6] = ((df.iloc[i, 2] - df.iloc[i, 4])+1)/2
        df.iloc[i, 7] = 0.5413
        if 'ipad' in df.iloc[i, 0].lower():
            df.iloc[i, 8] = 0.0703
        if 'music|tv|app store|icloud|ios' in df.iloc[i, 0].lower():
            df.iloc[i, 9] = 0.2205
        if 'mac' in df.iloc[i, 0].lower():
            df.iloc[i, 10] = 0.0756
    elif 'ipad' in df.iloc[i, 0].lower():
        df.iloc[i, 6] = ((df.iloc[i, 2] - df.iloc[i, 4])+1)/2
        df.iloc[i, 8] = 0.0703
        if 'music|tv|app store|icloud|ios' in df.iloc[i, 0].lower():
            df.iloc[i, 9] = 0.2205
        if 'mac' in df.iloc[i, 0].lower():
            df.iloc[i, 10] = 0.0756
    elif 'music|tv|app store|icloud|ios' in df.iloc[i, 0].lower():
        df.iloc[i, 6] = ((df.iloc[i, 2] - df.iloc[i, 4])+1)/2
        df.iloc[i, 9] = 0.2205
        if 'mac' in df.iloc[i, 0].lower():
            df.iloc[i, 10] = 0.0756
    elif 'mac' in df.iloc[i, 0].lower():
        df.iloc[i, 6] = ((df.iloc[i, 2] - df.iloc[i, 4])+1)/2
        df.iloc[i, 10] = 0.0756
    else:
        df.iloc[i, 6] = ((df.iloc[i, 2] - df.iloc[i, 4])+1)/2
        df.iloc[i, 11] = 0.0923
df = df.fillna(0)
for i in range(len(df)):
    df.iloc[i, 5] = df.iloc[i, 7] + df.iloc[i, 8] + df.iloc[i, 9] + df.iloc[i, 10] + df.iloc[i, 11]
    df.iloc[i, 6] = df.iloc[i, 6] * df.iloc[i, 5]
#new df with each mentioned category revenue percentage     
df = df.iloc[::-1].reset_index(drop=True)



#calculate the standardised combined score for each day
import datetime
import numpy as np

df['time']=pd.to_datetime(df['time'])

i = 0
mean_lst = [] ##mean of each day's comp  
per_lst = []
y = datetime.datetime.now()-datetime.timedelta(days=i)
sd = datetime.datetime(y.year, y.month, y.day, 0, 0, 0)
ed = datetime.datetime(y.year, y.month, y.day, 23, 59, 59)
while sd>=np.min(df['time']): ##compare the date to the earliest date of all reddits that have been captured
    y = datetime.datetime.now()-datetime.timedelta(days=i) ## separate each day
    sd = datetime.datetime(y.year, y.month, y.day, 0, 0, 0)
    ed = datetime.datetime(y.year, y.month, y.day, 23, 59, 59)
    a = np.mean((df[(sd <= df['time']) & (df['time'] <= ed)]['compound']))
    b = np.mean((df[(sd <= df['time']) & (df['time'] <= ed)]['per']))
    c = a/b
    mean_lst.append(c)
    i+=1

mean_lst = [x for x in mean_lst if not np.isnan(x)]
daylst = pd.to_datetime(df['time']).dt.date.unique().tolist()
mean_lst.reverse()
daylst.reverse()

data = {'Date':daylst, 'Mean':mean_lst}
new_df = pd.DataFrame(data)
new_df.to_csv('product_meanscores.csv', index=False)
