import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

#read the compound score file
csv_file = 'compound score files here'
df = pd.read_csv(csv_file).reset_index(drop=True)

#read AAPL stock
csv_file = 'apple stock price file here'
dfa = pd.read_csv(csv_file)
dfa['Date'] = pd.to_datetime(dfa['Date'])
dfa.set_index('Date', inplace=True)
nd = pd.date_range(start='2023-03-28', end='2023-06-26') #date this report analysed
dfa = dfa.reindex(nd)
dfa['Adj Close'].fillna(method='ffill', inplace=True)
dfa = dfa.loc['2023-03-28':'2023-06-26']
dfa = dfa.reset_index().rename(columns={'index': 'Date', 'Adj Close': 'Mean'})
dfa = dfa[['Date', 'Mean']]

#change here to change the lag day of backtest
lag = 2

#fine the dc points and local extremes
def ddcc(df, delta):
    
    dc_value = []
    dc_index = []
    le_value = []
    le_index = []
    trend = []

    delta = delta
    mode = 0
    le = df.iloc[0][1]
    le_value.append(le)
    le_index.append(df.iloc[0][0])
    for i in range(len(df)):
            if (df.iloc[i][1] / le) - 1 > delta and mode ==0:
                dc = df.iloc[i][1]
                dc_value.append(dc)
                dc_index.append(df.iloc[i][0])
                mode = 1
                trend.append(mode)
                le = dc

            if mode ==1:
                if df.iloc[i][1] >= le:
                    le = df.iloc[i][1]
                    a = df.iloc[i][0]

                if (df.iloc[i][1] / le) -1  < -(delta):
                    dc = df.iloc[i][1]
                    dc_value.append(dc)
                    dc_index.append(df.iloc[i][0])
                    le_value.append(le)
                    le_index.append(a)
                    mode = -1
                    trend.append(mode)

            if (df.iloc[i][1] / le) - 1 < -(delta) and mode ==0:
                dc = df.iloc[i][1]
                dc_value.append(dc)
                dc_index.append(df.iloc[i][0])
                mode = -1
                trend.append(mode)
                le = dc

            if mode == -1:
                if df.iloc[i][1] <= le:
                    le = df.iloc[i][1]
                    a = df.iloc[i][0]

                if (df.iloc[i][1] / le) - 1 > delta:
                    dc = df.iloc[i][1]
                    dc_value.append(dc)
                    dc_index.append(df.iloc[i][0])
                    le_value.append(le)
                    le_index.append(a)
                    mode = 1
                    trend.append(mode)
                    le = df.iloc[i][1]
                    a = df.iloc[i][0]

    plt.figure(figsize=(25, 15), dpi=50)
    ln1, = plt.plot(df['Date'][:], df['Mean'][:],'k*-',markersize=10, label = 'sentiment')
    ln2, = plt.plot(dc_index,dc_value,'rs',markersize=12, label = 'DC points')
    ln3, = plt.plot(le_index,le_value,'go-',markersize=10, label = 'local extremes')
    plt.legend(handles = [ln1, ln2, ln3], loc='upper right')
    plt.show()
    return le_index, le_value, trend, dc_index, dc_value


for dl in np.arange(0, 0.055, 0.005): #different delta level
    print('\n', dl)
    
    le_index, le_value, trend, dc_index, dc_value = ddcc(df,delta = dl)
    le_index1 = le_index
    le_value1 = le_value
    trend1 = trend
    dc_index1 = dc_index
    dc_value1 = dc_value
    
    data = {'Date':le_index1, 'Score':le_value1, 'Mode':trend1}
    ndf = pd.DataFrame(data)
    ndf['Date'] = pd.to_datetime(ndf['Date'])
    
    dfa = pd.merge(dfa, ndf, on='Date', how='outer')
    
    share =[]
    s = 0
    money = []
    m = 0
    dd = []
    l = len(dfa)
    f = 0
    
    #backtest strategy with money, share marketed
    for i in range(l):
        if dfa.iloc[i][3] == -1 & f == 1:
            if i+lag <= l-1:
                m += dfa.iloc[(i+lag)][1]
                money.append(m)
                s -= 1
                share.append(s)
                dd.append(dfa.iloc[(i+lag)][0])
                f -= 1
                   
        elif dfa.iloc[i][3] == 1:
            if i+lag <= l-1:
                m -= dfa.iloc[(i+lag)][1]
                money.append(m)
                s += 1
                share.append(s)
                dd.append(dfa.iloc[(i+lag)][0])
                f += 1
    
    r = {'Date':dd, 'Money1':money, 'Share1':share}
    result = pd.DataFrame(r)
    
    dfa = pd.merge(dfa, result, on='Date', how='outer')
    
    data = {'Date':dc_index1, 'DC': dc_value1, 'mode': trend1}
    dc = pd.DataFrame(data)
    dc['Date'] = pd.to_datetime(dc['Date'])
    dfa = pd.merge(dfa, dc, on='Date', how='outer')
    
    share =[]
    s = 0
    money = []
    m = 0
    dd = []
    l = len(dfa)
    
    for i in range(l):
        if dfa.iloc[i][7] == 1:
            if i+lag <= l-1:
                m += dfa.iloc[(i+lag)][1]
                money.append(m)
                s -= 1
                share.append(s)
                dd.append(dfa.iloc[(i+lag)][0])
                   
        elif dfa.iloc[i][7] == -1:
            if i+lag <= l-1:
                m -= dfa.iloc[(i+lag)][1]
                money.append(m)
                s += 1
                share.append(s)
                dd.append(dfa.iloc[(i+lag)][0])
    
    r = {'Date':dd, 'Money2':money, 'Share2':share}
    result = pd.DataFrame(r)
    dfa = pd.merge(dfa, result, on='Date', how='outer')
    dfa['Money1'].fillna(method='ffill',inplace=True)
    dfa['Money1'].fillna(value=0,inplace=True)
    dfa['Money2'].fillna(method='ffill',inplace=True)
    dfa['Money2'].fillna(value=0,inplace=True)
    dfa['Share1'].fillna(method='ffill',inplace=True)
    dfa['Share1'].fillna(value=0,inplace=True)
    dfa['Share2'].fillna(method='ffill',inplace=True)
    dfa['Share2'].fillna(value=0,inplace=True)
    
    #calculate the return le = le+lag day, dc= trading at the dc points
    x = dfa.iloc[-1][4] + (dfa.iloc[-1][1]*dfa.iloc[-1][5])
    y = dfa.iloc[-1][8] + (dfa.iloc[-1][1]*dfa.iloc[-1][9])
    print('le: ',x,'\nDC: ',y)
    
    
    #read the compound score file
    csv_file = 'compound score files here'
    df = pd.read_csv(csv_file).reset_index(drop=True)
    
    #read AAPL stock
    csv_file = 'apple stock price file here'
    dfa = pd.read_csv(csv_file)
    dfa['Date'] = pd.to_datetime(dfa['Date'])
    dfa.set_index('Date', inplace=True)
    nd = pd.date_range(start='2023-03-28', end='2023-06-26')
    dfa = dfa.reindex(nd)
    dfa['Adj Close'].fillna(method='ffill', inplace=True)
    dfa = dfa.loc['2023-03-28':'2023-06-26']
    dfa = dfa.reset_index().rename(columns={'index': 'Date', 'Adj Close': 'Mean'})
    dfa = dfa[['Date', 'Mean']]
