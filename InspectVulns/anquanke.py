import requests
from bs4 import BeautifulSoup as bs
import time
import pandas as pd
import os
import config
import storage_to_db


nowtime = '当前时间：<font size="3" color="red">' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '</font><br>'

def get_anquanke_info():
	url = 'https://www.anquanke.com/'
	keywords = config.keywords#关注的关键字
	wordlist = []
	select_msg = ''
	res = requests.get(url,timeout=60)
	#print(res.text)
	soup = bs(res.text,'html.parser')
	divs = soup.find_all('div',{'class':'title'})[0:9]
	spans = soup.find_all('span',{'class':'date'})
	#print(spans)
	#print(divs)
	for span in spans:
		date = span.find('span').text
	for div in divs:
		description = div.find('a').string
		#print(description)
		site = 'https://www.anquanke.com/' + div.find('a')['href']
		#print(site)
		for k in keywords:
			if k in description:
				keyword = k
				wordlist.append(keyword)
				data = {'description':description,'date':date}
				storage_to_db.storage_data(data)
				select_msg += '<p><b>发布日期：'+date+'</p></b>'+'<br><b>漏洞描述：</b>'+'<a href ="'+site\
        +'">'+description+ '</a></br>'
				break 
	if divs is None:
		msg = nowtime + '<p>今日安全客风和日丽，无大事发生!!!</p>'
		dataframe = pd.DataFrame({'Anquanke告警总数':[0],'Anquanke检索数':[0]})
		dataframe.to_csv(os.path.join(config.output_path, 'An_quan_ke_data.csv'),encoding="gb2312")
		return msg

	else:
		msg_header = '<p>今日安全客一共<font size="3" color="red">' + str(len(divs))+'</font>条。'
		if len(wordlist) == 0:
			key_msg = '根据设置的关键字，未匹配到关注的安全客信息。</p>'
			msg = nowtime + msg_header + key_msg
			dataframe = pd.DataFrame({'Anquanke告警总数':[len(divs)],'Anquanke检索数':[0]})
			dataframe.to_csv(os.path.join(config.output_path, 'An_quan_ke_data.csv'),encoding="gb2312")
			return msg
		else:
			key_msg = '</p>根据设置的关键字，关注的安全客信息一共<font size="3" color="red">' + str(len(wordlist))+'</font>个。具体如下：<br><br>'
			msg = nowtime + msg_header + key_msg + select_msg
			dataframe = pd.DataFrame({'Anquanke告警总数':[len(divs)],'Anquanke检索数':[len(wordlist)]})
			dataframe.to_csv(os.path.join(config.output_path, 'An_quan_ke_data.csv'),encoding="gb2312")
			return msg



if __name__ == '__main__':
	get_anquanke_info()