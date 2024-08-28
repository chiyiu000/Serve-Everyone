# -*- coding: utf-8 -*-
import os, sys
import pandas as pd
import matplotlib.pyplot as plt
            
#计算n天内的最大值和最小值
def max_min_range(arrPrices, iStart, iWin):

    data_win_low = []
    data_win_high = []
    
    if iStart - iWin < 0 :
        j = k = 0
        for j in range(iStart):
            data_win_low.append(df.iloc[j]['low'])
        for k in range(iStart):
            data_win_high.append(df.iloc[k]['high'])
    elif iStart + iWin >= len(arrPrices) - 1:
        j = k = 0
        for j in range(len(arrPrices) - iStart ):
            data_win_low.append(df.iloc[iStart + j]['low'])
        for k in range(len(arrPrices) - iStart ):
            data_win_high.append(df.iloc[iStart + k]['high'])
    else:
        j = k = 0
        for j in range(iWin):
            data_win_low.append(df.iloc[iStart - iWin + j]['low'])
        for k in range(iWin):
            data_win_high.append(df.iloc[iStart - iWin + k]['high'])

    #监视哨算法求最大最小值
    Ln = data_win_low[0]
    Hn = data_win_high[0]
    for x1 in data_win_low:
        if x1 < Ln:
            Ln = x1
    for y1 in data_win_high:
        if y1 > Hn:
            Hn = y1
    return Ln, Hn

#fcode = '600362'
#fcode = '600519'
fcode = '300359'
#fcode = '300059'
#fcode = '300052'

## dataFrame  数据加载
df = pd.read_csv('./' + fcode + '.csv', parse_dates=True, index_col=0)

#df.head(5) # 预览前5行数据
#df.describe() # 数据基本统计量

# 画收盘价5,10,20日移动平均线  
df['Ma5'] = df['close'].rolling(window=5).mean()
df['Ma10'] = df['close'].rolling(window=10).mean()
df['Ma20'] = df['close'].rolling(window=20).mean()
df['MA_Cross']=0

#MA10从第10天开始
j = 11
#判断均线金叉，用1表示金叉，-1表示死叉
for i in range(len(df)-12):
    if df.iloc[j]['Ma5'] >= df.iloc[j]['Ma10'] and df.iloc[j+1]['Ma5'] > df.iloc[j+1]['Ma10'] and df.iloc[j-1]['Ma5'] < df.iloc[j-1]['Ma10'] :
        df.loc[j, 'MA_Cross'] = 1
        plt.text(x=j,#文本x轴坐标 
        y = df.iloc[j]['Ma5'], #文本y轴坐标
        s = 'G', #文本内容         
        fontdict=dict(fontsize=12, color='r',family='monospace',)#字体属性字典
        )
        print('Find a gold MA_Cross!\n')
    if df.iloc[j]['Ma5'] <= df.iloc[j]['Ma10'] and df.iloc[j+1]['Ma5']*1.01 < df.iloc[j+1]['Ma10'] and df.iloc[j-1]['Ma5'] > df.iloc[j-1]['Ma10'] :
        df.loc[j, 'MA_Cross'] = -1
        plt.text(x = j,#文本x轴坐标 
        y = df.iloc[j]['Ma5'], #文本y轴坐标
        s = 'D', #文本内容         
        fontdict=dict(fontsize=12, color='r',family='monospace',)#字体属性字典
        )
        print('Find a death MA_Cross!\n')
    j = j + 1#

#KDJ指标计算
#9日RSV=（C-L9）/（H9-L9）×100
#式中，C为第9日的收盘价；L9为9日内的最低价；H9为9日内的最高价。
#K值=2/3×前一日K值＋1/3×当日RSV
#D值=2/3×前一日D值＋1/3×当日K值
#J值=3D—2K
df['RSV'] = 0
df['K'] = 0
df['D'] = 0
df['J'] = 0
for i in range(len(df)):
    if i == 0:
        df.loc[i, 'RSV'] = 50
        df.loc[i, 'K'] = 50
        df.loc[i, 'D'] = 50
        df.loc[i, 'J'] = 50
    else:
        L9, H9 = max_min_range(df, i, 9)
        df.loc[i, 'RSV'] =  (df.iloc[i]['close'] - L9) / (H9 - L9) * 100
        df.loc[i, 'K'] = 0.667 * df.iloc[i-1]['K'] + 0.333 * df.iloc[i]['RSV']
        df.loc[i, 'D'] = 0.667 * df.iloc[i-1]['D'] + 0.333 * df.iloc[i]['K']
        df.loc[i, 'J'] = 3 * df.iloc[i]['K'] - 2 * df.iloc[i]['D']

#数金叉和死叉
df['kdj_Cross'] = 0
#在第一个子图中画出均线指标
fig = plt.figure( )  #定义画布
ax1 = fig.add_subplot(3, 1, 1)  #2行1列排布子图，该为第1个子图
df[['close', 'Ma5', 'Ma10', 'Ma20']].plot(ax = ax1, figsize=(12,6), grid=True, title=fcode + 'price and MA-5-10-20')

#在第二个子图中画出KDJ指标
ax2 = fig.add_subplot(3, 1, 2)  #2行1列排布子图，该为第2个子图
df[['K','D']].plot(ax = ax2, figsize=(12,6), grid=True, title=fcode + ' KDJ Indexs')
df[['J']].plot(ax = ax2, figsize=(12,6), color='m', grid=True, title=fcode + ' KDJ Indexs')
#KDJ从第2天开始
j = 1
#判断均线金叉，用1表示金叉，-1表示死叉
for i in range(len(df)-2):
    if df.iloc[j]['K'] >= df.iloc[j]['D'] and df.iloc[j+1]['K'] > df.iloc[j+1]['D'] and df.iloc[j-1]['K'] < df.iloc[j-1]['D'] :
        df.loc[j, 'kdj_Cross'] = 1
        plt.text(x=j,#文本x轴坐标 
        y = df.iloc[j]['D'], #文本y轴坐标
        s = 'G', #文本内容         
        fontdict=dict(fontsize=12, color='r',family='monospace',)#字体属性字典
        )
        print('Find a gold KDJcross!\n')
    if df.iloc[j]['K'] <= df.iloc[j]['D'] and df.iloc[j+1]['K']*1.01 < df.iloc[j+1]['D'] and df.iloc[j-1]['K'] > df.iloc[j-1]['D'] :
        df.loc[j, 'kdj_Cross'] = -1
        plt.text(x = j,#文本x轴坐标 
        y = df.iloc[j]['D'], #文本y轴坐标
        s = 'D', #文本内容         
        fontdict=dict(fontsize=12, color='r',family='monospace',)#字体属性字典
        )
        print('Find a death cross!\n')
    j = j + 1


#画收盘价12,26日指数移动平均线 
df['EMA_12'] = pd.DataFrame.ewm(df['close'], span=12).mean()
df['EMA_26'] = pd.DataFrame.ewm(df['close'], span=26).mean()

#MACD指标计算
df['DIF'] = df['EMA_12'] - df['EMA_26']
df['DEA'] = pd.DataFrame.ewm(df['DIF'], span=9).mean()
df['MACD'] = 2 * (df['DIF'] - df['DEA'])
df['MACD_P'] = 0
df['MACD_N'] = 0
k = 0
for k in range(len(df)-1):
    if df.iloc[k]['MACD'] >= 0:
        df.loc[k, 'MACD_P'] = df.iloc[k]['MACD']
    else:
        df.loc[k, 'MACD_N'] = df.iloc[k]['MACD']
#数金叉和死叉
df['macd_Cross'] = 0

#在第三个子图中画出MACD指标
ax2 = fig.add_subplot(3, 1, 3)  #3行1列排布子图，该为第2个子图
df[['DIF']].plot(ax = ax2, figsize=(12,6), color='b', grid=True, title=fcode + ' MACD Indexs')
df[['DEA']].plot(ax = ax2, figsize=(12,6), color='y', grid=True, title=fcode + ' MACD Indexs')
df['MACD_P'].plot(ax = ax2, color='r', kind='bar')
df['MACD_N'].plot(ax = ax2, color='g', kind='bar')
j = 1
#判断均线金叉，用1表示金叉，-1表示死叉
for i in range(len(df)-2):
    if df.iloc[j]['DIF'] >= df.iloc[j]['DEA'] and df.iloc[j+1]['DIF'] > df.iloc[j+1]['DEA'] and df.iloc[j-1]['DIF'] < df.iloc[j-1]['DEA'] :
        df.loc[j, 'macd_Cross'] = 1
        plt.text(x=j,#文本x轴坐标 
        y = df.iloc[j]['DEA'], #文本y轴坐标
        s = 'G', #文本内容         
        fontdict=dict(fontsize=14, color='r',family='monospace',)#字体属性字典
        )
        print('Find a gold cross!\n')
    if df.iloc[j]['DIF'] <= df.iloc[j]['DEA'] and df.iloc[j+1]['DIF']*1.01 < df.iloc[j+1]['DEA'] and df.iloc[j-1]['DIF'] > df.iloc[j-1]['DEA'] :
        df.loc[j, 'macd_Cross'] = -1
        plt.text(x = j,#文本x轴坐标 
        y = df.iloc[j]['DEA'], #文本y轴坐标
        s = 'D', #文本内容         
        fontdict=dict(fontsize=14, color='r',family='monospace',)#字体属性字典
        )
        print('Find a death macd_Cross!\n')
    j = j + 1

print(df)
#目标涨幅
df['up_10'] = 0
df['up_20'] = 0
df['up_60'] = 0
for i in range(len(df)):
    if i <len(df)-60:
        print(str(df.loc[i+10, 'close'])+"-"+str(df.loc[i, 'close']))
        df.loc[i, 'up_10'] = (df.loc[i+10, 'close']-df.loc[i, 'close'])/1.0*df.loc[i, 'close']
        df.loc[i, 'up_20'] = (df.loc[i+20, 'close']-df.loc[i, 'close'])/1.0*df.loc[i, 'close']
        df.loc[i, 'up_60'] = (df.loc[i+60, 'close']-df.loc[i, 'close'])/1.0*df.loc[i, 'close']
    elif i <len(df)-20:
        df.loc[i, 'up_20'] = (df.loc[i+20, 'close']-df.loc[i, 'close'])/1.0*df.loc[i, 'close']
        df.loc[i, 'up_10'] = (df.loc[i+10, 'close']-df.loc[i, 'close'])/1.0*df.loc[i, 'close']
    elif i <len(df)-10:
        df.loc[i,'up_10'] = (df.loc[i+10, 'close']-df.loc[i, 'close'])/1.0*df.loc[i, 'close']
print(df.head(30))
df.to_csv(fcode + '_MA_KDJ_MACD.csv')

plt.show()

'''
#回测交易，从死叉开始，找离他最近的那个金叉进行买入，以死叉的价格卖出
#计算近120个交易日内的金叉和死叉投资回报
totalprofit = 100
backtrackstart = len(df) - 240
buySignal = True   #记录买入卖出信号
#crossbuy = 0
crossbuy = df.iloc[backtrackstart]['open']
profitlist = []
while backtrackstart < len(df):
    #print(str(backtrackstart))
    if df.iloc[backtrackstart]['Cross'] == 1 :
        crossbuy = df.iloc[backtrackstart]['open']   #金叉的当天开盘买入
        buySignal = True
    if  buySignal and df.iloc[backtrackstart]['Cross'] == -1 :
        totalprofit = totalprofit *(1 + (df.iloc[backtrackstart]['close'] - crossbuy) / crossbuy)    #计算以死叉当天收盘价卖出的收益
        print("The total profit is " + str(totalprofit))
        profitlist.append(totalprofit)
        buySignal = False
    backtrackstart = backtrackstart + 1

#从不空仓
if buySignal :
    totalprofit = totalprofit *(1 + (df.iloc[-1]['close'] - crossbuy) / crossbuy)    #最后一天收盘价卖出的收益
    profitlist.append(totalprofit)
    buySignal = False

print("The total profit is " + str(totalprofit))


#显示收益曲线
dfprofit = pd.DataFrame(profitlist)
dfprofit.to_csv(fcode + 'profit.csv')
dfprofit.plot(subplots=False, figsize=(12,6), grid=True, title=fcode + '_profit')

'''
