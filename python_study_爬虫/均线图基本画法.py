# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import matplotlib.pyplot as plt

fcode = '002594'
# dataFrame  数据加载
df = pd.read_csv(r'D:\tushare的数据\修改后的数据\002594.csv', parse_dates=[3])

df.head() # 预览前5行数据
df.describe() # 数据基本统计量



#df.plot(figsize=(12,6), grid=True, legend=jz, label='66001'+str(i))  

# 画收盘价5,10,20日移动平均线  
df['Ma5'] = df['close'].rolling(window=5).mean()
df['Ma10'] = df['close'].rolling(window=10).mean()
df['Ma20'] = df['close'].rolling(window=20).mean()

df[['close','Ma5','Ma10','Ma20']].plot(subplots=False, figsize=(12,6), grid=True, title=fcode)
plt.show()

f2 = 'MA_'+ fcode + '.png'
plt.savefig(f2)
plt.close()