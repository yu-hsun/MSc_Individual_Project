##chinese analysis sentiment model
from transformers import BertTokenizer, BertForSequenceClassification
import pandas as pd
from scipy.special import softmax
import numpy as np
import datetime

#MacBERT
model_name = 'hfl/chinese-roberta-wwm-ext' 

tokenizer = BertTokenizer.from_pretrained(model_name)
model = BertForSequenceClassification.from_pretrained(model_name)
model.eval()

#pre-process data and get sentiment scores
def sentiments(x):
    reddit = x.replace('\n',' ')
    reddit_words = []
    for i in reddit.split(' '):
        if i.startswith('@') and len(i) > 1:
            i = '@使用者'
        elif i.startswith('http'):
            i = 'http'
        reddit_words.append(i)
        
    reddit_proc = ' '.join(reddit_words)
    
    #load model and tokenizer (neg and pos)    
    lables = ['neg', 'pos']
    
    ##sentiment analysis
    encoded_reddit = tokenizer(reddit_proc, return_tensors='pt')
    if len(x) >= 513:
        score = [0.0, 0.0]
    else:           
        output = model(**encoded_reddit)
        score = output[0][0].detach().numpy()
        score = softmax(score)
    
    result = {'lable': lables, 'score': score}
    dfr = pd.DataFrame(result)
    return dfr

def get_day_means(df):
    #create new DataFrame dic
    data_dict = {
        'title': [],
        'time': [],
        'pos': [],
        'neg': []
    }
    
    #put the scores, content and time into a dic
    for i in range(len(df)):
        sentiment = sentiments(df.iloc[i][0])
        data_dict['title'].append(df.iloc[i][0])
        data_dict['time'].append(df.iloc[i][1])
        data_dict['pos'].append(sentiment.iloc[1][1])
        data_dict['neg'].append(sentiment.iloc[0][1])
        print(i)
    new_df = pd.DataFrame(data_dict)
    
    df = new_df
    df['time']=pd.to_datetime(df['time'])
    
    #calculate the mean compound score of each day
    i = 0
    mean_lst = [] #mean of each day's comp    
    y = datetime.datetime.now()-datetime.timedelta(days=i)
    sd = datetime.datetime(y.year, y.month, y.day, 0, 0, 0)
    ed = datetime.datetime(y.year, y.month, y.day, 23, 59, 59)
    while sd>=np.min(df['time']): #compare the date to the earliest date of all reddits that have been captured
        y = datetime.datetime.now()-datetime.timedelta(days=i) ## separate each day
        sd = datetime.datetime(y.year, y.month, y.day, 0, 0, 0)
        ed = datetime.datetime(y.year, y.month, y.day, 23, 59, 59)
        a = np.mean(df[(sd <= df['time']) & (df['time'] <= ed)]['pos'])
        b = np.mean(df[(sd <= df['time']) & (df['time'] <= ed)]['neg'])
        #compound scores:((pos-neg)+1)/2
        c = ((a-b)+1)/2
        mean_lst.append(c)
        i+=1
    
    #finalise data arrangement  
    mean_lst = [x for x in mean_lst if not np.isnan(x)]    
    daylst = pd.to_datetime(df['time']).dt.date.unique().tolist()
    mean_lst.reverse()
    daylst.reverse()
    return daylst, mean_lst, new_df

dfc = pd.read_csv('chinese_reddit.csv')   
daylstc, mean_lstc, new_dfc = get_day_means(dfc)
data = {'Date':daylstc,'Mean':mean_lstc}
df_final = pd.DataFrame(data)
new_dfc.to_csv('chinese_reddit_scores.csv', index=False)
df_final.to_csv('chinese_reddit_meanscores.csv', index=False)
