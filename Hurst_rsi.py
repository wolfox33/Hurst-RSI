# -*- coding: utf-8 -*-
"""
Created on Mon Nov 22 22:35:16 2021

@author: Leopoldo
"""

from pandas_datareader import data as wb
import numpy as np
import matplotlib.pyplot as plt
import pandas as pd
from hurst import compute_Hc
import ta



start = '2015-1-1'
end = '2022-1-1'
ativo = 'BTC-USD'
df = wb.DataReader(ativo, data_source='yahoo', start= start, end= end )
df.rename(columns={'Close': 'close'}, inplace=True)

series=df.close
H = compute_Hc(series, kind='price')[0]

print("Hurst Exponent H={:.4f}".format(H))
plt.figure(figsize=(8,5))
plt.title('Preço')
plt.plot(df.close.tail(len(df)-120))

df['H']=0

for i in range(120,len(df)):
    df.H.iloc[i]=compute_Hc(df.close.iloc[i-120:i-1], kind='price',simplified=False)[0]
plt.figure(figsize=(8,5))
plt.title('Hurst')
df.H.tail(len(df)-120).plot()
plt.axhline(0.50,color='g')

df['Signal']= 0
df['Signal']=np.where( df.H>0.50,1,df.Signal)


df['RSI'] = ta.momentum.rsi(df.close,14)
#(df.close.shift(1).values,14)


df['Return']=df.close.pct_change().shift(-1)

#regras somente para a compra
df['StrReturn']=0
df['StrReturn']= np.where(((df.RSI>50) & (df.Signal==1)),df.Return,df.StrReturn)

total_slippage_cost=len(df[df.StrReturn!=0])*0.05/df.close.mean()
total_slippage_cost



Cumulative_Returns = np.cumprod(df.StrReturn + 1)-1

plt.figure(figsize=(8,5))
plt.title('Retorno acumulado da estratégia ')
Cumulative_Returns.tail(len(df)-120).plot()

Final_percentage_retuns=(Cumulative_Returns.iloc[-1]-total_slippage_cost)*100

Final_percentage_retuns
