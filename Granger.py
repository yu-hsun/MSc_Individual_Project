import pandas as pd
from statsmodels.tsa.stattools import grangercausalitytests

csv_file = 'mean_score files'

df = pd.read_csv(csv_file).reset_index(drop=True)
df = df.rename(columns={'Mean':'Score'})
df['Date'] = pd.to_datetime(df['Date'])
df.set_index('Date', inplace=True)

#date this report analysed
df = df.loc['2023-03-28':'2023-06-26']
dfp = df.reset_index().rename(columns={'index': 'Date', 'Score': 'Mean'})
df = df.reset_index().rename(columns={'index': 'Date', 'Score': 'Score'})

csv_file = 'apple stock price file'
dfa = pd.read_csv(csv_file)
dfa['Date'] = pd.to_datetime(dfa['Date'])
dfa.set_index('Date', inplace=True)

nd = pd.date_range(start='2023-03-28', end='2023-06-26')
dfa = dfa.reindex(nd)
#fill the non-open date with the latest previous adjust close price
dfa['Adj Close'].fillna(method='ffill', inplace=True)
dfa = dfa.loc['2023-03-28':'2023-06-26']
dfa = dfa.reset_index().rename(columns={'index': 'Date', 'Adj Close': 'Mean'})
dfa = dfa[['Date', 'Mean']]

df = pd.concat([df, dfa['Mean']],axis=1)

#get the result of granger causality tests analysing 5-day lag
result = grangercausalitytests(df[['Score', 'Mean']], maxlag=5)
