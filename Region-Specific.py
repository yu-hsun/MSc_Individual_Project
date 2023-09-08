import datetime
import pandas as pd

#read english reddit with count of each day's data amount file
df1 = pd.read_csv('english_withcount.csv')
df1['Date'] = pd.to_datetime(df1['Date'])
df1.set_index('Date', inplace=True)
df1 = df1.loc['2023-03-28':'2023-06-26']
df1 = df1.reset_index().rename(columns={'Date': 'Date', 'Mean': 'Mean_E', 'Count': 'Count_E'})

#read chinese reddit with count of each day's data amount file
df2 = pd.read_csv('chinese_withcount.csv')
df2['Date'] = pd.to_datetime(df2['Date'])

#merge two data by date
df = pd.merge(df1, df2, on='Date', how='outer')

lst1=[]

#calculate the standardised combined score for each day
for i in range(len(df)):
    x = df.iloc[i,1]*((0.3984+0.2525)/2)*(df.iloc[i,2]/(df.iloc[i,2] + df.iloc[i,4]))
    y = df.iloc[i,3]*0.1878*(df.iloc[i,4]/(df.iloc[i,2] + df.iloc[i,4]))
    lst1.append(x+y)
                      
                      

data = {'Date':df['Date'], 'Mean':lst1}
new_df = pd.DataFrame(data)
new_df.to_csv('region_meanscores.csv', index=False)
