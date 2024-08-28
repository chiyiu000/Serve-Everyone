import tushare as ts
pro=ts.pro_api('1fa028915f0f2aa941f12676c69d25564c04ad3db9843d4fd0dfa657')
import pandas as pd
#单个股票
sigleStock=pro.daily(ts_code='002594.SZ', start_date='20230101', end_date='20240510')
#多个股票
#mulStock = pro.daily(ts_code='601985.SH,000002.SZ', start_date='20200701', end_date='20210722')
#print(sigleStock)
#print(mulStock)
#sigleStock.sort_values('trade_date', inplace=True,ascending=False)

sigleStock.to_csv(r'D:\tushare的数据\tushare爬取的数据\002594 daily.csv')
#sigleStock=sigleStock[['trade_date','low']]#数据清洗
#sigleStock.to_csv(r'D:\tushare的数据\已清洗的数据\300410(已清洗).csv')