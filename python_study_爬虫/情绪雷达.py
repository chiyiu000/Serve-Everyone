import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
plt.rcParams['font.sans-serif'] = ['Microsoft YaHei']
file_path = "D:/股民情感分析/分析数据/002594.csv"
data = pd.read_csv(file_path)

# 分类情绪值
conditions = [
    (data['情绪'] <= 0.33),
    (data['情绪'] > 0.33) & (data['情绪'] <= 0.66),
    (data['情绪'] > 0.66) & (data['情绪'] <= 1),
]
choices = ['消极', '中立', '积极']
data['情绪分类'] = np.select(conditions, choices)

# 计算每个类别的数量
emotion_counts = data['情绪分类'].value_counts().reindex(choices, fill_value=0)

# 绘制雷达图
labels=np.array(choices)
stats=emotion_counts.values

angles=np.linspace(0, 2*np.pi, len(labels), endpoint=False).tolist()

#为了闭合雷达图，将stats和angles的第一个元素添加到它们各自的末尾。
stats=np.concatenate((stats,[stats[0]]))
angles+=angles[:1]

#创建一个雷达图的子图，设置背景为极坐标，并填充区域，
fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))
ax.fill(angles, stats, color='red', alpha=0.25)
ax.set_yticklabels([])
ax.set_xticks(angles[:-1])
ax.set_xticklabels(labels)

#设置图表的标题，并展示雷达图。
plt.title('情绪雷达图', size=10)
plt.show()