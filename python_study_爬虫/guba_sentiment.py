#导入相关库
import requests
from bs4 import BeautifulSoup
import pandas as pd
from snownlp import SnowNLP

headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/85.0.4183.102 Safari/537.36'} 
#请求数据，定义函数
def getHTMLText(url):
	r=requests.get(url, headers = headers)
	r.encoding=r.apparent_encoding
	text=r.text
	return text

#解析单个网页，并提取数据字段
def getOnePageInfo(url):
	one_page_data=[]
	text = getHTMLText(url)
	# print(text)
	soup=BeautifulSoup(text,'html.parser')
	post_list=soup.find_all('tr',class_="listitem") #找到所有的帖子所在标签
	print(post_list)
	for post in post_list:
		read_counts=post.find('div', class_='read').text #获取帖子阅读数
		comment_counts=post.find('div', class_='reply').text #获取帖子评论数
		title=post.find('div', class_='title').text #获取帖子标题
		# author_id=post.find('div', class_='author cl').find('a').text #获取作者id
		# time=post.find('div',class_='update mod_time').text #获取更新时间
		# data=[read_counts,comment_counts,title,author_id,time]

		data=[read_counts,comment_counts,title]
		one_page_data.append(data)
	return one_page_data
#循环获取多页信息（以1-10页为例）
all_data=[]
for i in range(1, 40):
    # url=f'https://guba.eastmoney.com/list,zssh000001_{i}.html'
    url=f'https://guba.eastmoney.com/list,600029_{i}.html'
    print(url)
    one_page_data=getOnePageInfo(url)
    all_data.extend(one_page_data) #extend可以添加列表
#将数据存储至csv文件中
# all_data=pd.DataFrame(all_data,columns=['阅读数','评论数','标题','作者','最后更新'])
all_data=pd.DataFrame(all_data,columns=['阅读数','评论数','标题'])
#all_data.to_csv(r'D:\股吧爬虫\不加入情感分析的数据\600028帖子test.csv')
#使用SnowNLP计算对每个帖子标题的文字评估情绪得分
def senti(text):
    s=SnowNLP(text)
    return s.sentiments
all_data['情绪']=all_data['标题'].apply(senti)
all_data.to_csv(r'D:\python 爬虫的50种数据\600029帖子+情感test.csv')
