#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd
import numpy as np
import os
import sklearn.preprocessing

import scipy.stats
import math

import matplotlib.pyplot as plt
import matplotlib

from datetime import datetime


# In[2]:


# to show the whole datafram when use .head()
pd.set_option('display.max_columns',1000)
pd.set_option('display.max_rows',1000)
pd.set_option('display.width', 10000)


# In[84]:


path = 'ticks_201910/'

path_image = 'GroupOne/report_plots/'


# In[4]:


#path = r'/Users/sujiaqi/Desktop/last semester courses/jgl/project/ticks_201910'
list_VXX = []
list_SPY = []
list_VXX_date = []
list_SPY_date = []
for (root, dirs, files) in os.walk(path):
    for file in files:
        Dr_type = file.split("_")[1]
        #print(Dr_type)
        if Dr_type == 'VXX':
            list_VXX.append(file)
            date = file.split("_")[2].split(".")[0]
            list_VXX_date.append(date)
        elif Dr_type == 'SPY':
            list_SPY.append(file)
            date = file.split("_")[2].split(".")[0]
            list_SPY_date.append(date)


# In[5]:


list_SPY.sort()
list_VXX.sort()
list_SPY_date.sort()
list_VXX_date.sort()


# In[47]:


list_SPY_date


# In[6]:


vxx_df = pd.read_csv(path + 'tick_VXX_'+ '20191001' +'.txt', header = None)
spy_df = pd.read_csv(path + 'tick_SPY_'+ '20191001' +'.txt', header = None)

vxx_df = vxx_df[[0,5]]
spy_df = spy_df[[0,5]]

vxx_df.rename(columns={0:'date', 5:'price_vxx'}, inplace = True)
spy_df.rename(columns={0:'date', 5:'price_spy'}, inplace = True)

spy_vxx_df = pd.merge(vxx_df, spy_df, on=['date'], how="outer",sort=True)  
spy_vxx_df.ffill(axis = 0, inplace = True)

spy_vxx_df.dropna(inplace = True)
spy_vxx_df.reset_index(drop = True,inplace=True)

spy_vxx_df['time'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[1])
spy_vxx_df['date'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[0])

spy_vxx_df['vxx_pct_chg'] = spy_vxx_df["price_vxx"].pct_change()
spy_vxx_df['spy_pct_chg'] = spy_vxx_df["price_spy"].pct_change()

spy_vxx_df.dropna(inplace = True)


# In[7]:


spy_vxx_df.head()


# In[8]:


spy_vxx_df.head()


# In[9]:


#spy_vxx_df['next_time'] = spy_vxx_df['time'].shift(-1)


# In[10]:


# spy_vxx_df['time_diff'] = np.nan

# for i in range(1, len(spy_vxx_df['time']), 1):
#     spy_vxx_df['time_diff'][i] = (60*60* (int(spy_vxx_df['next_time'][i].split(':',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[0])) 
#                            + 60*(int(spy_vxx_df['next_time'][i].split(':',2)[1]) - int(spy_vxx_df['time'][1].split(':',2)[1]))
#                            + int(spy_vxx_df['next_time'][i].split(':',2)[2].split('.',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[0])
#                            + math.pow(10, -len(spy_vxx_df['next_time'][i].split(':',2)[2].split('.', 2)[1])) * int(spy_vxx_df['next_time'][i].split(':',2)[2].split('.',2)[1]) - math.pow(10, -len(spy_vxx_df['time'][1].split(':',2)[2].split('.', 2)[1]))* int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[1]))


# In[80]:


for date in list_SPY_date:
    
    vxx_df = pd.read_csv(path + 'tick_VXX_'+ date +'.txt', header = None)
    spy_df = pd.read_csv(path + 'tick_SPY_'+ date +'.txt', header = None)

    vxx_df = vxx_df[[0,5]]
    spy_df = spy_df[[0,5]]

    vxx_df.rename(columns={0:'date', 5:'price_vxx'}, inplace = True)
    spy_df.rename(columns={0:'date', 5:'price_spy'}, inplace = True)

    spy_vxx_df = pd.merge(vxx_df, spy_df, on=['date'], how="outer",sort=True)  
    spy_vxx_df.ffill(axis = 0, inplace = True)

    spy_vxx_df.dropna(inplace = True)
    spy_vxx_df.reset_index(drop = True,inplace=True)

    spy_vxx_df['time'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[1])
    spy_vxx_df['date'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[0])

    spy_vxx_df['vxx_pct_chg'] = spy_vxx_df["price_vxx"].pct_change()
    spy_vxx_df['spy_pct_chg'] = spy_vxx_df["price_spy"].pct_change()

    spy_vxx_df.dropna(inplace = True)
    
    
    spy_vxx_df['seconds'] = np.nan

    for i in range(1, len(spy_vxx_df['time']), 1):
        spy_vxx_df['seconds'][i] = (60*60* (int(spy_vxx_df['time'][i].split(':',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[0])) 
                               + 60*(int(spy_vxx_df['time'][i].split(':',2)[1]) - int(spy_vxx_df['time'][1].split(':',2)[1]))
                               + int(spy_vxx_df['time'][i].split(':',2)[2].split('.',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[0])
                               + math.pow(10, -len(spy_vxx_df['time'][i].split(':',2)[2].split('.', 2)[1])) * int(spy_vxx_df['time'][i].split(':',2)[2].split('.',2)[1]) - math.pow(10, -len(spy_vxx_df['time'][1].split(':',2)[2].split('.', 2)[1]))* int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[1]))
        
    time_list = []
    vxx_price_chg_list = []
    spy_price_chg_list = []
    
    for i in range(1, len(spy_vxx_df['seconds']), 1):
   
        j = i
        while ((spy_vxx_df['seconds'][j+1] - spy_vxx_df['seconds'][i]) < 0.01):
            j=j+1
        
        
        vxx_price_chg = spy_vxx_df['price_vxx'][j] - spy_vxx_df['price_vxx'][i]
        spy_price_chg = spy_vxx_df['price_spy'][j] - spy_vxx_df['price_spy'][i]
        if (vxx_price_chg > 0):    
            time_list.append(spy_vxx_df['seconds'][j])
            spy_price_chg_list.append(spy_price_chg)
            vxx_price_chg_list.append(vxx_price_chg)
        
 
    corr = np.correlate(vxx_price_chg_list, spy_price_chg_list)[0]


    print('Date: ', date)
    print('Correlation between Price Change of VXX and SPY:', corr)
    
    plt.figure(figsize=(20, 10))
    #plt.subplot(end_wk-start_wk+1, 1,week-14)

    plt.plot(time_list, vxx_price_chg_list, color='green', marker='o', 
         linestyle='dashdot', linewidth=1, markersize=2, label = 'vxx_price_chg_10_msec')
    
    plt.plot(time_list,spy_price_chg_list, color='red', marker='+', 
         linestyle='dotted', linewidth=1, markersize=2, label = 'spy_price_chg_10_msec')

    plt.xlabel('time_in_seconds')
    plt.ylabel('Price Change of VXX and SPY within 10 msec')
    #plt.rcParams['figure.figsize'] = (22.0, 16.0)

    plt.legend()
    plt.title('Price Change of VXX and SPY within 10 msec in date  '+ str(date), fontsize ='large', fontweight='bold')
    
    plt.savefig(path_image + 'Price Change of VXX and SPY within 10 msec in date  '+ str(date) + '.png')
    plt.show()
    


# In[50]:


colums_list = ['date', 'corr_per_min', 'corr_per_hour']
corr_df = pd.DataFrame(np.nan,columns = colums_list, index = range(1,len(list_SPY_date)+1,1))


# In[51]:


corr_df['date'] = list_SPY_date


# In[52]:


corr_df


# In[81]:


corr_list = []
for date in list_SPY_date:
    
    vxx_df = pd.read_csv(path + 'tick_VXX_'+ date +'.txt', header = None)
    spy_df = pd.read_csv(path + 'tick_SPY_'+ date +'.txt', header = None)

    vxx_df = vxx_df[[0,5]]
    spy_df = spy_df[[0,5]]

    vxx_df.rename(columns={0:'date', 5:'price_vxx'}, inplace = True)
    spy_df.rename(columns={0:'date', 5:'price_spy'}, inplace = True)

    spy_vxx_df = pd.merge(vxx_df, spy_df, on=['date'], how="outer",sort=True)  
    spy_vxx_df.ffill(axis = 0, inplace = True)

    spy_vxx_df.dropna(inplace = True)
    spy_vxx_df.reset_index(drop = True,inplace=True)

    spy_vxx_df['time'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[1])
    spy_vxx_df['date'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[0])

    spy_vxx_df['vxx_pct_chg'] = spy_vxx_df["price_vxx"].pct_change()
    spy_vxx_df['spy_pct_chg'] = spy_vxx_df["price_spy"].pct_change()

    spy_vxx_df.dropna(inplace = True)
    
    
    spy_vxx_df['seconds'] = np.nan

    for i in range(1, len(spy_vxx_df['time']), 1):
        spy_vxx_df['seconds'][i] = (60*60* (int(spy_vxx_df['time'][i].split(':',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[0])) 
                               + 60*(int(spy_vxx_df['time'][i].split(':',2)[1]) - int(spy_vxx_df['time'][1].split(':',2)[1]))
                               + int(spy_vxx_df['time'][i].split(':',2)[2].split('.',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[0])
                               + math.pow(10, -len(spy_vxx_df['time'][i].split(':',2)[2].split('.', 2)[1])) * int(spy_vxx_df['time'][i].split(':',2)[2].split('.',2)[1]) - math.pow(10, -len(spy_vxx_df['time'][1].split(':',2)[2].split('.', 2)[1]))* int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[1]))
        
    
    time_list = []
    vxx_price_chg_list = []
    spy_price_chg_list = []
    
    
    
#     for i in range(1, len(spy_vxx_df['seconds']), 3600):
   
#         j = i
    
    max_sec = max(spy_vxx_df['seconds'])
    counter = int(max_sec/3600)
    timestamp_list = []
    
    for i in range(1, counter+1, 1):       
        for j in range(1, len(spy_vxx_df['seconds']), 1):         
            if (spy_vxx_df['seconds'][j] > 3600*i):
                timestamp_list.append(j)
                break
    
    timestamp_list.insert(0, 1)
    
    for i in range(0, len(timestamp_list)-1, 1):
        
        now = timestamp_list[i]
        after = timestamp_list[i+1]
        
        vxx_price_chg = spy_vxx_df['price_vxx'][after] - spy_vxx_df['price_vxx'][now]
        spy_price_chg = spy_vxx_df['price_spy'][after] - spy_vxx_df['price_spy'][now]
        
        vxx_price_chg_list.append(vxx_price_chg)
        spy_price_chg_list.append(spy_price_chg)
        
        time_list.append(after)

       
 
    corr = np.corrcoef(vxx_price_chg_list, spy_price_chg_list)[0][1]
    corr_list.append(corr)

    print('Date: ', date)
    print('Correlation between Price Change of VXX and SPY:', corr)
    
    plt.figure(figsize=(20, 10))
    #plt.subplot(end_wk-start_wk+1, 1,week-14)

    plt.plot(time_list, vxx_price_chg_list, color='green', marker='o', 
         linestyle='dashdot', linewidth=1, markersize=5, label = 'vxx_price_chg_per_hour')
    
    plt.plot(time_list,spy_price_chg_list, color='red', marker='+', 
         linestyle='dotted', linewidth=1, markersize=5, label = 'spy_price_chg_per_hour')

    plt.xlabel('time_in_seconds')
    plt.ylabel('Price Change of VXX and SPY per hour')
    #plt.rcParams['figure.figsize'] = (22.0, 16.0)

    plt.legend()
    plt.title('Price Change of VXX and SPY per hour in date  '+ str(date), fontsize ='large', fontweight='bold')
    
    plt.savefig(path_image + 'Price Change of VXX and SPY per hour in date '+ str(date) + '.png')
    plt.show()
    


# In[54]:


corr_df['corr_per_hour'] = corr_list


# In[82]:


corr_list_2 = []

for date in list_SPY_date:
    
    vxx_df = pd.read_csv(path + 'tick_VXX_'+ date +'.txt', header = None)
    spy_df = pd.read_csv(path + 'tick_SPY_'+ date +'.txt', header = None)

    vxx_df = vxx_df[[0,5]]
    spy_df = spy_df[[0,5]]

    vxx_df.rename(columns={0:'date', 5:'price_vxx'}, inplace = True)
    spy_df.rename(columns={0:'date', 5:'price_spy'}, inplace = True)

    spy_vxx_df = pd.merge(vxx_df, spy_df, on=['date'], how="outer",sort=True)  
    spy_vxx_df.ffill(axis = 0, inplace = True)

    spy_vxx_df.dropna(inplace = True)
    spy_vxx_df.reset_index(drop = True,inplace=True)

    spy_vxx_df['time'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[1])
    spy_vxx_df['date'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[0])

    spy_vxx_df['vxx_pct_chg'] = spy_vxx_df["price_vxx"].pct_change()
    spy_vxx_df['spy_pct_chg'] = spy_vxx_df["price_spy"].pct_change()

    spy_vxx_df.dropna(inplace = True)
    
    
    spy_vxx_df['seconds'] = np.nan

    for i in range(1, len(spy_vxx_df['time']), 1):
        spy_vxx_df['seconds'][i] = (60*60* (int(spy_vxx_df['time'][i].split(':',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[0])) 
                               + 60*(int(spy_vxx_df['time'][i].split(':',2)[1]) - int(spy_vxx_df['time'][1].split(':',2)[1]))
                               + int(spy_vxx_df['time'][i].split(':',2)[2].split('.',2)[0]) - int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[0])
                               + math.pow(10, -len(spy_vxx_df['time'][i].split(':',2)[2].split('.', 2)[1])) * int(spy_vxx_df['time'][i].split(':',2)[2].split('.',2)[1]) - math.pow(10, -len(spy_vxx_df['time'][1].split(':',2)[2].split('.', 2)[1]))* int(spy_vxx_df['time'][1].split(':',2)[2].split('.',2)[1]))
        
    
    time_list = []
    vxx_price_chg_list = []
    spy_price_chg_list = []
    
    
    
#     for i in range(1, len(spy_vxx_df['seconds']), 3600):
   
#         j = i
    
    max_sec = max(spy_vxx_df['seconds'])
    counter = int(max_sec/60)
    timestamp_list = []
    
    for i in range(1, counter+1, 1):       
        for j in range(1, len(spy_vxx_df['seconds']), 1):         
            if (spy_vxx_df['seconds'][j] > 60*i):
                timestamp_list.append(j)
                break
    
    timestamp_list.insert(0, 1)
    
    for i in range(0, len(timestamp_list)-1, 1):
        
        now = timestamp_list[i]
        after = timestamp_list[i+1]
        
        vxx_price_chg = spy_vxx_df['price_vxx'][after] - spy_vxx_df['price_vxx'][now]
        spy_price_chg = spy_vxx_df['price_spy'][after] - spy_vxx_df['price_spy'][now]
        
        vxx_price_chg_list.append(vxx_price_chg)
        spy_price_chg_list.append(spy_price_chg)
        
        time_list.append(after)

       
 
    corr = np.corrcoef(vxx_price_chg_list, spy_price_chg_list)[0][1]
    corr_list_2.append(corr)


    print('Date: ', date)
    print('Correlation between Price Change of VXX and SPY:', corr)
    
    plt.figure(figsize=(20, 10))
    #plt.subplot(end_wk-start_wk+1, 1,week-14)

    plt.plot(time_list, vxx_price_chg_list, color='green', marker='o', 
         linestyle='dashdot', linewidth=1, markersize=3, label = 'vxx_price_chg_per_minute')
    
    plt.plot(time_list,spy_price_chg_list, color='red', marker='+', 
         linestyle='dotted', linewidth=1, markersize=3, label = 'spy_price_chg_per_minute')

    plt.xlabel('time_in_seconds')
    plt.ylabel('Price Change of VXX and SPY per minute')
    #plt.rcParams['figure.figsize'] = (22.0, 16.0)

    plt.legend()
    plt.title('Price Change of VXX and SPY per minute in date '+ str(date), fontsize ='large', fontweight='bold')
    
    plt.savefig(path_image + 'Price Change of VXX and SPY per minute in date '+ str(date) + '.png')

    plt.show()
    
    


# In[59]:


len(corr_list)


# In[62]:


len(corr_list[24:])


# In[63]:


corr_df['corr_per_min'] = corr_list[24:]


# In[66]:


corr_df.dropna(inplace=True)


# In[75]:


corr_df['corr_per_min'].mean()


# In[76]:


corr_df['corr_per_hour'].mean()


# In[71]:


import pylab as pl


# In[86]:


plt.figure(figsize=(20, 10))
#plt.subplot(end_wk-start_wk+1, 1,week-14)

plt.plot(corr_df['date'], corr_df['corr_per_min'], color='green', marker='o', 
     linestyle='dashdot', linewidth=1, markersize=3, label = 'corr_per_min')

plt.plot(corr_df['date'],corr_df['corr_per_hour'], color='red', marker='+', 
     linestyle='dotted', linewidth=1, markersize=3, label = 'corr_per_hour')

pl.xticks(corr_df['date'], rotation=75)

plt.xlabel('date')
plt.ylabel('Correlation between Price Change of VXX and SPY per minute/hour')
#plt.rcParams['figure.figsize'] = (22.0, 16.0)

plt.legend()
plt.title('Correlation between Price Change of VXX and SPY per minute/hour in 24 trading days', fontsize ='large', fontweight='bold')
plt.savefig(path_image + 'Correlation_between_Price_Change_of_VXX_and_SPY_per_minute_hour_in_24_trading_days.png')

plt.show()


# In[ ]:





# In[44]:


corr_list = [x for x in corr_list if str(x) != 'nan']


# In[45]:


corr_list


# In[39]:


np.mean(corr_list)


# In[27]:


np.corrcoef(vxx_price_chg_list, spy_price_chg_list)[0][1]


# In[18]:


vxx_price_chg_list


# In[19]:


spy_price_chg_list


# In[87]:


for date in list_SPY_date:
    vxx_df = pd.read_csv(path + 'tick_VXX_'+ date +'.txt', header = None)
    spy_df = pd.read_csv(path + 'tick_SPY_'+ date +'.txt', header = None)
    
    vxx_df = vxx_df[[0,5]]
    spy_df = spy_df[[0,5]]
    
    vxx_df.rename(columns={0:'date', 5:'price_vxx'}, inplace = True)
    spy_df.rename(columns={0:'date', 5:'price_spy'}, inplace = True)
    
    spy_vxx_df = pd.merge(vxx_df, spy_df, on=['date'], how="outer",sort=True)  
    spy_vxx_df.ffill(axis = 0, inplace = True)
    
    # spy_vxx_df.to_csv('spy_vxx_price_'+ date +'.csv')
    
    spy_vxx_df.dropna(inplace = True)
    
    spy_vxx_df.reset_index(drop = True,inplace=True)
    
    spy_vxx_df['time'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[1])
    spy_vxx_df['date'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[0])
    
    spy_vxx_df['vxx_pct_chg'] = spy_vxx_df["price_vxx"].pct_change()
    spy_vxx_df['spy_pct_chg'] = spy_vxx_df["price_spy"].pct_change()
    
    
    spy_vxx_df.dropna(inplace = True)
    
    corr_list = []
    for i in range(1,len(spy_vxx_df['vxx_pct_chg'])+1,1):
        corr = np.correlate(spy_vxx_df['vxx_pct_chg'][i:], spy_vxx_df['spy_pct_chg'][:-(i-1)])[0]
        i = i + 1
        corr_list.append(corr)
    
    
    spy_vxx_df['correlation_delay_vxx'] = corr_list
    print('Date: ', date)
    print('maximum negative correlation is ', min(corr_list))
    print('vxx delayed ticket number is ', corr_list.index(min(corr_list)))
    print('maximum positive correlation is ', max(corr_list))
    print('vxx delayed ticket number is ', corr_list.index(max(corr_list)))
    
    plt.figure(figsize=(20, 10))
    #plt.subplot(end_wk-start_wk+1, 1,week-14)
    plt.plot(range(1,len(spy_vxx_df['correlation_delay_vxx'])+1,1), spy_vxx_df['correlation_delay_vxx'],color='green', marker='o', 
         linestyle='dashdot', linewidth=1, markersize=3, label = 'correlation_delay_vxx')
    
    plt.xlabel('VXX Lagged Ticket Numbers')
    plt.ylabel('Correlation when VXX Delayed')
    #plt.rcParams['figure.figsize'] = (22.0, 16.0)
    plt.legend()
    plt.title('Plot of Correlation between SPY and lagged VXX '+ str(date), fontsize ='large', fontweight='bold')
    plt.savefig(path_image + 'Correlation_between_SPY_and_lagged_VXX_in_date_'+ str(date) + '.png')

    plt.show()


# In[6]:


for date in list_SPY_date:
    vxx_df = pd.read_csv(path + 'tick_VXX_'+ date +'.txt', header = None)
    spy_df = pd.read_csv(path + 'tick_SPY_'+ date +'.txt', header = None)
    
    vxx_df = vxx_df[[0,5]]
    spy_df = spy_df[[0,5]]
    
    vxx_df.rename(columns={0:'date', 5:'price_vxx'}, inplace = True)
    spy_df.rename(columns={0:'date', 5:'price_spy'}, inplace = True)
    
    spy_vxx_df = pd.merge(vxx_df, spy_df, on=['date'], how="outer",sort=True)  
    spy_vxx_df.ffill(axis = 0, inplace = True)
    
    # spy_vxx_df.to_csv('spy_vxx_price_'+ date +'.csv')
    
    spy_vxx_df.dropna(inplace = True)
    
    spy_vxx_df.reset_index(drop = True,inplace=True)
    
    spy_vxx_df['time'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[1])
    spy_vxx_df['date'] = spy_vxx_df['date'].map(lambda x: x.split(' ')[0])
    
    spy_vxx_df.dropna(inplace = True)
    
    
    plt.figure(figsize=(20, 10))
    #plt.subplot(end_wk-start_wk+1, 1,week-14)
    plt.plot(range(1,len(spy_vxx_df['price_spy'])+1,1), spy_vxx_df['price_spy'],color='green', marker='o', 
         linestyle='dashdot', linewidth=1, markersize=3, label = 'price_spy')
    
    plt.xlabel('time')
    plt.ylabel('price')
    #plt.rcParams['figure.figsize'] = (22.0, 16.0)
    plt.legend()
    plt.title('Plot of Price SPY '+ str(date), fontsize ='large', fontweight='bold')
    
    plt.xlabel('time')
    plt.ylabel('price')
    #plt.rcParams['figure.figsize'] = (22.0, 16.0)
    plt.legend()
    plt.title('Plot of Price SPY '+ str(date), fontsize ='large', fontweight='bold')
    
    plt.show()
    
    


# In[ ]:




