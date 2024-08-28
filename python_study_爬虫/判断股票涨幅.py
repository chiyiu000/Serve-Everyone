import pandas as pd
import mplfinance as mpf
import pandas as pd
df = pd.read_csv(r'D:\tushare的数据\MA EMA MACD KDJ数据表\002594 Ma EMa KDJ.csv', parse_dates=[1])
df['up_10'] = 0
df['up_20'] = 0
df['up_60'] = 0
for i in range(len(df)):
    if i <len(df)-60:
        print(str(df.loc[i+10, 'close'])+"-"+str(df.loc[i, 'close']))
        df.loc[i, 'up_10'] = (df.loc[i+10, 'close']-df.loc[i, 'close'])/df.loc[i, 'close']
        df.loc[i, 'up_20'] = (df.loc[i+20, 'close']-df.loc[i, 'close'])/df.loc[i, 'close']
        df.loc[i, 'up_60'] = (df.loc[i+60, 'close']-df.loc[i, 'close'])/df.loc[i, 'close']
    elif i <len(df)-20:
        df.loc[i, 'up_20'] = (df.loc[i+20, 'close']-df.loc[i, 'close'])/df.loc[i, 'close']
        df.loc[i, 'up_10'] = (df.loc[i+10, 'close']-df.loc[i, 'close'])/df.loc[i, 'close']
    elif i <len(df)-10:
        df.loc[i,'up_10'] = (df.loc[i+10, 'close']-df.loc[i, 'close'])/df.loc[i, 'close']
print(df.head(30))
df.to_csv(r'D:\tushare的数据\修改后的数据\002594.csv')
#*df.loc[i, 'close']