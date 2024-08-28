import pandas as pd

df = pd.read_csv(r'D:\tushare的数据\tushare爬取的数据\002594 daily.csv', parse_dates=[1])
df.sort_values('trade_date',inplace=True)
df.to_csv(r'D:\tushare的数据\排列好的顺序\002594 daily.csv')
