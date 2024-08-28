import pandas as pd
import mplfinance as mpf

df = pd.read_csv(r'D:\tushare的数据\修改后的数据\002594.csv',parse_dates=[3])
df.set_index('trade_date',inplace=True) 
df.head(3)
df.tail(3)
mpf.plot(
    data=df.head(100),
    type="candle",
    title="Candlestick for 000869",
    ylabel="price(RMB)",
    style="binance",
    ylabel_lower="vol(shares)"
)