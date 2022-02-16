# -*- coding: utf-8 -*-
"""
Created on Sun Sep 27 12:26:48 2020

@author: pavel_000
"""

'''
Description of financial markets
'''

#%% Major indices

import yfinance as yf
import datetime as dt
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib as mpl
pd.set_option('display.max_columns', None)


# downloading the tickers


try:
    indices = pd.read_html('https://finance.yahoo.com/world-indices')[0]
except: #if the website were to change
    indices = pd.DataFrame(data = np.array([    ['^GSPC', 'S&P 500'],
                                       ['^DJI', 'Dow 30'],
                                       ['^IXIC', 'Nasdaq'],
                                       ['^NYA', 'NYSE COMPOSITE (DJ)']
                                           ]),
                           columns = ['Symbol', 'Name']
                                       )
    
indices.info()
indices = indices[['Symbol','Name']].astype('string')
indices

#downloading the data for all indices
start_date = '1980-01-01'
end_date = dt.datetime.today()

data = yf.download(list(indices['Symbol']), start = start_date, end = end_date, frequency = 'D') 
data.info()
data.columns #its in a form of a multiindex
data.columns.get_level_values(0) #gets the first level
data.columns.get_level_values(1)
list(data.columns.get_level_values(0)) # all columns

prices = data['Adj Close']
prices.info()
prices.dropna(thresh = 252 * 20, axis = 1, inplace = True) #drop if history for less than 20yrs

prices.head()
prices = round(prices, 2)
prices.describe()

MaxStd = pd.DataFrame(prices.describe().loc['std'])[pd.DataFrame(prices.describe().loc['std']) == prices.describe().loc['std'].max()].dropna()
MinStd = pd.DataFrame(prices.describe().loc['std'])[pd.DataFrame(prices.describe().loc['std']) == prices.describe().loc['std'].min()].dropna()

MaxStd['Name'] = indices.loc[indices['Symbol'] == MaxStd.index[0], 'Name'].values
MinStd['Name'] = indices.loc[indices['Symbol'] == MinStd.index[0], 'Name'].values

print('The biggest standard deviation of all indices has %s (Ticker: %s) with a value of %.2f'%( MaxStd['Name'][0], MaxStd.index[0] , MaxStd['std']))
print('The smallest standard deviation of all indices has %s (Ticker: %s) with a value of %.2f'%( MinStd['Name'][0], MinStd.index[0] , MinStd['std']))

prices = prices.fillna(method = 'ffill')

fig, ax = plt.subplots(figsize = (13, 6))
for i in range(int(len(prices.columns)/2)):
    ax.plot(prices.iloc[:, i], label = prices.columns[i])
fig.legend(loc = 0)
labels = ax.get_xticklabels()
plt.setp(labels, rotation = 45, horizontalalignment= 'right')
ax.yaxis.set_major_formatter(mpl.ticker.StrMethodFormatter("{x:,.0f}"))
ax.set_title('First %d indices'%int(len(prices.columns)/2))


returns = pd.DataFrame()

for i in range(0, len(prices.columns)):
    returns[prices.columns[i]] = prices.iloc[:, i] / prices.iloc[:, i].shift(1)


tot_rtn = pd.DataFrame()

#biggest gainer since inception
for i in range(0, len(prices.columns)):
    if prices.columns[i] == '^BVSP': continue
    tot_rtn[prices.columns[i]] = [prices.loc[prices.iloc[:,i].last_valid_index()][i]/ prices.loc[prices.iloc[:,i].first_valid_index()][i]]
tot_rtn = round(tot_rtn, 4)


fig, ax = plt.subplots(figsize = (12, 6))
ax.barh(list(tot_rtn.columns), list(tot_rtn.iloc[0]))
ax.set_title('total returns in % since inception')




