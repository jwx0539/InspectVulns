import requests 
from bs4 import BeautifulSoup as bs
import pandas as pd
import time
import os
import config
import storage_to_db


nowtime = '当前时间：<font size="3" color="red">' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '</font><br>'


def get_hacker_news_info():
	url = 'https://thehackernews.com/'
	keywords = config.keywords #关注的关键字
	wordlist = []
	select_msg = ''
	res = requests.get(url=url,timeout=60)
	#print(res.text)
	soup = bs(res.text,'html.parser')
	h2s = soup.find_all('h2',{'align':'justify'})
	total_hacker_news = len(h2s)
	spans = soup.find_all('span',{'class':'dtstamp author'})
	#print(spans)
	for span in spans:
		date = span.find('meta')['content']
		#print(date)
	for h2 in h2s:
		site = h2.find('a')['href']
		description = h2.find('a').string
		for k in keywords:
			if k in description:
				keyword = k
				wordlist.append(keyword)
				data = {'description':description,'date':date}
				storage_to_db.storage_data(data)
				select_msg += '<p><b>发布日期：'+date+'</p></b>'+'<br><b>漏洞描述：</b>'+'<a href ="'+site\
        +'">'+description+ '</a></br>'
				break 
		#print(description)


	if h2s is None:
		msg = nowtime + '<p>今日Hacker_news风和日丽，无大事发生!!!</p>'
		dataframe = pd.DataFrame({'hacker_news告警总数':[0],'hacker_news检索数':[0]})
		dataframe.to_csv(os.path.join(config.output_path, 'hacker_news_data.csv'),encoding="gb2312")
		return msg

	else:
		msg_header = '<p>今日Hacker_news一共<font size="3" color="red">' + str(len(h2s))+'</font>条。'
		if len(wordlist) == 0:
			key_msg = '根据设置的关键字，未匹配到关注的Hacker_news信息。</p>'
			msg = nowtime + msg_header + key_msg
			dataframe = pd.DataFrame({'hacker_news告警总数':[len(h2s)],'hacker_news检索数':[0]})
			dataframe.to_csv(os.path.join(config.output_path, 'hacker_news_data.csv'),encoding="gb2312")
			return msg
		else:
			key_msg = '</p>根据设置的关键字，关注的Hacker_news信息一共<font size="3" color="red">' + str(len(wordlist))+'</font>个。具体如下：<br><br>'
			msg = nowtime + msg_header + key_msg + select_msg
			dataframe = pd.DataFrame({'hacker_news告警总数':[len(h2s)],'hacker_news检索数':[len(wordlist)]})
			dataframe.to_csv(os.path.join(config.output_path, 'hacker_news_data.csv'),encoding="gb2312")
			return msg



if __name__ == '__main__':
	get_hacker_news_info()