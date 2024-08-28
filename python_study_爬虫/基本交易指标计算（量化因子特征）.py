import tushare as ts
pro=ts.pro_api('1fa028915f0f2aa941f12676c69d25564c04ad3db9843d4fd0dfa657')
import os
import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r'D:\tushare的数据\排列好的顺序\002594 daily.csv', parse_dates=[1])

# ========== 计算移动平均线
# 分别计算5日、10日、20日的移动平均线
Ma_list = [5, 10, 20]

# 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
for Ma in Ma_list:
    df['Ma' + str(Ma)] = df['close'].rolling(Ma).mean()

df['MA_Cross']=0
#MA10从第10天开始
j = 11
#判断均线金叉，用1表示金叉，-1表示死叉
for i in range(len(df)-12):
    if df.iloc[j]['Ma5'] >= df.iloc[j]['Ma10'] and df.iloc[j+1]['Ma5'] > df.iloc[j+1]['Ma10'] and df.iloc[j-1]['Ma5'] < df.iloc[j-1]['Ma10'] :
        df.loc[j, 'MA_Cross'] = 1
        #df.iloc[j]['Cross'] = 1
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
    j = j + 1

print(df.tail(100))
#df.to_csv(r'D:\tushare的数据\金叉死叉\600519 金叉死叉.csv')

# 计算指数平滑移动平均线EMa
EMa_list=[12,26]
for EMa in EMa_list:
    df['EMA_' + str(EMa)] = pd.DataFrame.ewm(df['close'], span=EMa).mean()

df['DIF'] = df['EMA_' + str(12)] - df['EMA_' + str(26)]
df['DEA'] = pd.DataFrame.ewm(df['DIF'], span=9).mean()
df['MACD'] = 2 * (df['DIF'] - df['DEA'])
df['MACD_Cross']=0
j=1
for i in range(len(df)-2):
    if df.iloc[j]['DIF'] >= df.iloc[j]['DEA'] and df.iloc[j+1]['DIF'] > df.iloc[j+1]['DEA'] and df.iloc[j-1]['DIF'] < df.iloc[j-1]['DEA'] :
        df.loc[j, 'MACD_Cross'] = 1
#        plt.text(x=j,#文本x轴坐标 
#        y = df.iloc[j]['DEA'], #文本y轴坐标
#        s = 'G', #文本内容         
#        fontdict=dict(fontsize=14, color='r',family='monospace',)#字体属性字典
#        )
        print('Find a gold MACD_Cross!\n')
    if df.iloc[j]['DIF'] <= df.iloc[j]['DEA'] and df.iloc[j+1]['DIF']*1.01 < df.iloc[j+1]['DEA'] and df.iloc[j-1]['DIF'] > df.iloc[j-1]['DEA'] :
        df.loc[j, 'MACD_Cross'] = -1
#        plt.text(x = j,#文本x轴坐标 
#        y = df.iloc[j]['DEA'], #文本y轴坐标
#        s = 'D', #文本内容         
#        fontdict=dict(fontsize=14, color='r',family='monospace',)#字体属性字典
#        )
        print('Find a death MACD_Cross!\n')
    j = j + 1
    print(j)
df.to_csv(r'D:\tushare的数据\加入MACD_Cross的数据\002594 MACD.csv')
print(df.tail(10))

#计算RSV指标
#计算n天内的最大值和最小值
def max_min_range(arrPrices, iStart, iWin):
    data_win_low = []
    data_win_high = []
    
    if iStart - iWin < 0 :
        j = k = 0
        for j in range(iStart):
            data_win_low.append(df.iloc[j]['low'])
            j = j + 1
        for k in range(iStart):
            data_win_high.append(df.iloc[k]['high'])
            k = k + 1
    elif iStart + iWin >= len(arrPrices) - 1:
        j = k = 0
        for j in range(len(arrPrices) - iStart ):
            data_win_low.append(df.iloc[iStart + j]['low'])
            j = j + 1
        for k in range(len(arrPrices) - iStart ):
            data_win_high.append(df.iloc[iStart + k]['high'])
            k = k + 1
    else:
        j = k = 0
        for j in range(iWin):
            data_win_low.append(df.iloc[iStart - iWin + j]['low'])
            j = j + 1
        for k in range(iWin):
            data_win_high.append(df.iloc[iStart - iWin + k]['high'])
            k = k + 1
    print(data_win_low)
    print(data_win_high)
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

#计算KDJ指标
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

df['KDJ_Cross'] = 0
#在第一个子图中画出均线指标
#fig = plt.figure( )  #定义画布
#ax1 = fig.add_subplot(3, 1, 1)  #2行1列排布子图，该为第1个子图
#df[['close', 'Ma5', 'Ma10', 'Ma20']].plot(ax = ax1, figsize=(12,6), grid=True, title=fcode + 'price and MA-5-10-20')

#在第二个子图中画出KDJ指标
#ax2 = fig.add_subplot(3, 1, 2)  #2行1列排布子图，该为第2个子图
#df[['K','D']].plot(ax = ax2, figsize=(12,6), grid=True, title=fcode + ' KDJ Indexs')
#df[['J']].plot(ax = ax2, figsize=(12,6), color='m', grid=True, title=fcode + ' KDJ Indexs')
#KDJ从第2天开始
j = 1
#判断均线金叉，用1表示金叉，-1表示死叉
for i in range(len(df)-2):
    if df.iloc[j]['K'] >= df.iloc[j]['D'] and df.iloc[j+1]['K'] > df.iloc[j+1]['D'] and df.iloc[j-1]['K'] < df.iloc[j-1]['D'] :
#        df.loc[j, 'KDJ_Cross'] = 1
#        plt.text(x=j,#文本x轴坐标 
#        y = df.iloc[j]['D'], #文本y轴坐标
#        s = 'G', #文本内容         
#        fontdict=dict(fontsize=12, color='r',family='monospace',)#字体属性字典
#        )
        print('Find a gold KDJ_Cross!\n')
    if df.iloc[j]['K'] <= df.iloc[j]['D'] and df.iloc[j+1]['K']*1.01 < df.iloc[j+1]['D'] and df.iloc[j-1]['K'] > df.iloc[j-1]['D'] :
        df.loc[j, 'KDJ_Cross'] = -1
#        plt.text(x = j,#文本x轴坐标 
#        y = df.iloc[j]['D'], #文本y轴坐标
#        s = 'D', #文本内容         
#        fontdict=dict(fontsize=12, color='r',family='monospace',)#字体属性字典
#        )
        print('Find a death KDJ_Cross!\n')
    j = j + 1


# ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
df.to_csv(r'D:\tushare的数据\MA EMA MACD KDJ数据表\002594 Ma EMa KDJ.csv', index=False)