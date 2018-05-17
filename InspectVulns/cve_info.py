import re
import time
import storage_to_db
import requests
import pandas as pd
import os
import config
from bs4 import BeautifulSoup as bs

nowtime = '当前时间：<font size="3" color="red">' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '</font><br>'


def get_CVE_urls():
    urls = []
    res = requests.get('https://cassandra.cerias.purdue.edu/CVE_changes/today.html')
    #print(res.text)
    targets = re.findall(r"New entries:(.*?)Graduations",res.text,re.S|re.M)
    for target in targets:
        soup = bs(target,'html.parser')
        tags = soup.find_all('a')
        #print(urls)
        for i in tags:
            url = i['href']
            urls.append(url)
        return urls

def get_CVE_info():  
    urls = get_CVE_urls()
    select_msg = ''
    wordlist = []
    keywords = config.keywords
    if(len(urls)==0):
        msg = nowtime + '<p>今日CVE_today风和日丽，无大事发生!!!</p>'
        dataframe = pd.DataFrame({'CVE_info告警总数':[0],'CVE_info检索数':[0]})
        dataframe.to_csv(os.path.join(config.output_path, 'cve_info_data.csv'),encoding="gb2312")
        return msg
    else:
        msg_header = '<p>今日CVE_today一共<font size="3" color="red">' + str(len(urls))+'</font>个。'
        for url in urls:
            res = requests.get(url, timeout=60)
            soup = bs(res.text, 'html.parser')
            cveId = soup.find(nowrap='nowrap').find('h2').string
            table = soup.find(id='GeneratedTable').find('table')
            company = table.find_all('tr')[8].find('td').string
            createdate = table.find_all('tr')[10].find('td').string
            description = table.find_all('tr')[3].find('td').text
            for k in keywords:
                if k in description:
                    keyword = k
                    wordlist.append(keyword)
                    data = {'cveid':cveId,'keyword':k,'company':company,'description':description,'createdate':createdate}
                    storage_to_db.storage_data(data)
                    select_msg += '<p><b>漏洞编号：</b><a href="'+ url +'">'+cveId+'</a></p><b>相关厂商：</b>'\
                    +company +'<br><b>披露日期：</b>'\
                    +createdate+'<br><b>关键字：</b><font size="3" color="red">'\
                    +keyword+'</font><br><b>漏洞描述：</b>'\
                    +description + '<br><br><hr/>'
                    break
            
        if len(wordlist) == 0:
                key_msg = '根据设置的关键字，未匹配到关注的CVE信息。</p>'
                msg = nowtime + msg_header + key_msg
                dataframe = pd.DataFrame({'CVE_info告警总数':[len(urls)],'CVE_info检索数':[0]})
                dataframe.to_csv(os.path.join(config.output_path, 'cve_info_data.csv'),encoding="gb2312")
                return msg
        else:
            key_msg = '</p>根据设置的关键字，关注的CVE信息一共有CVE<font size="3" color="red">' + str(len(wordlist))+'</font>个。具体如下：<br><br>'
            msg = nowtime + msg_header + key_msg +select_msg
            dataframe = pd.DataFrame({'CVE_info告警总数':[len(urls)],'CVE_info检索数':[len(wordlist)]})
            dataframe.to_csv(os.path.join(config.output_path, 'cve_info_data.csv'),encoding="gb2312")
            return msg

if __name__ == '__main__':
    get_CVE_info()
    