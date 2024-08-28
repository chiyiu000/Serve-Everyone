# -*- coding: utf-8 -*-
import pandas as pd

# ========== 从原始csv文件中导入股票数据，以浦发银行sh600059为例
# 导入数据 - 注意：这里请填写数据文件在您电脑中的路径
stock_data = pd.read_csv(r'D:\tushare的数据\tushare爬取的数据\300750 daily.csv', parse_dates=[1])
# 将数据按照交易日期从远到近排序
stock_data.sort_values('trade_date', ascending=False)

# ========== 计算移动平均线
# 分别计算5日、20日、60日的移动平均线
ma_list = [5, 20, 60]

# 计算简单算术移动平均线MA - 注意：stock_data['close']为股票每天的收盘价
for ma in ma_list:
    stock_data['MA_' + str(ma)] = stock_data['close'].rolling(ma).mean()

# 计算指数平滑移动平均线EMA
EMa_list=[12,26]
for EMa in EMa_list:
    stock_data['EMA_' + str(EMa)] = pd.DataFrame.ewm(stock_data['close'], span=EMa).mean()

# 将数据按照交易日期从近到远排序
stock_data.sort_values('trade_date', ascending=False, inplace=True)

# ========== 将算好的数据输出到csv文件 - 注意：这里请填写输出文件在您电脑中的路径
stock_data.to_csv(r'D:\tushare的数据\MA EMA MACD KDJ数据表\300750 MA ema2.csv', index=False)