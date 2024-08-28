import pandas as pd
import mplfinance as mpf
import matplotlib.pyplot as plt
# 设置支持中文的字体
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']  # 或者使用其他支持中文的字体，如'Microsoft YaHei'
plt.rcParams['axes.unicode_minus'] = False  # 用来正常显示负号
# 数据
df = pd.read_csv(r'D:\加入时间的股吧爬虫数据\600028帖子+情感_t.csv', parse_dates=[4])

emotion_values = df['情绪']
count_0_to_0_33=0
count_0_33_to_0_66=0
count_0_66_to_1=0

for value in emotion_values:
    if 0<=value<0.33:
        count_0_to_0_33+=1
    elif 0.33<=value<=0.66:
        count_0_33_to_0_66+=1
    elif 0.66<=value<=1:
        count_0_66_to_1+=1
print(f"情绪价值在0~0.33的个数：{count_0_to_0_33}")
print(f"情绪价值在0.33~0.66的个数：{count_0_33_to_0_66}")
print(f"情绪价值在0.33~0.66的个数：{count_0_66_to_1}")

df['category'] = pd.cut(emotion_values, bins =  [0, 0.33, 0.66, 1], 
                    labels = ['0-0.33情绪低迷股民', '0.33-0.66中立股民', '0.66-1情绪高昂股民'])

total = df['category'].value_counts(normalize = True) * 100

fontdict=dict(fontsize=12, color='r',family='monospace',)

plt.figure(figsize = (8, 8))
plt.pie(total, labels = total.index,autopct = '%1.2f%%',startangle = 90)
plt.axis('equal')
plt.title("中国石化股民情绪分析图")
plt.show()

df.to_csv(r'D:\股民情感分析\分析数据\600028.csv')

