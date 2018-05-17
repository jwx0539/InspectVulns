import os
import config
import pandas as pd
import numpy as np
from pyecharts import Bar
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei']  # 指定默认字体
plt.rcParams['axes.unicode_minus'] = False  # 解决保存图像是负号'-'显示为方块的问题

def get_echart_bar():
    df_cve_info = pd.read_csv('./output/cve_info_data.csv',encoding="gb2312")
    total_CVE = df_cve_info.loc[0].iloc[1]
    key_CVE = df_cve_info.loc[0].iloc[2]

    df_exploit_db = pd.read_csv('./output/exploit_db_data.csv',encoding="gb2312")
    total_exploit_db = df_exploit_db.loc[0].iloc[1]
    key_exploit_db = df_exploit_db.loc[0].iloc[2]

    df_hacker_news = pd.read_csv('./output/hacker_news_data.csv',encoding="gb2312")
    total_hacker_news = df_hacker_news.loc[0].iloc[1]
    key_hacker_news = df_hacker_news.loc[0].iloc[2]

    df_threat_book = pd.read_csv('./output/threat_book_data.csv',encoding="gb2312")
    total_threat_book = df_threat_book.loc[0].iloc[1]
    key_threat_book = df_threat_book.loc[0].iloc[2]

    df_anquanke = pd.read_csv('./output/An_quan_ke_data.csv',encoding="gb2312")
    total_anquanke = df_anquanke.loc[0].iloc[1]
    key_anquanke = df_anquanke.loc[0].iloc[2]

    attr = ["CVE漏洞", "Exploit_db告警",'hacker_news消息','threat_book情报','Anquanke资讯']
    v1 = [total_CVE,total_exploit_db,total_hacker_news,total_threat_book,total_anquanke]
    v2 = [key_CVE,key_exploit_db,key_hacker_news,key_threat_book,key_anquanke]
    bar = Bar("今日漏洞告警")
    bar.add("漏洞预警总数", attr, v1)
    bar.add("漏洞检索数", attr, v2)
    bar.render()
    print('[]**********************图表已经生成')


def get_plt_bar():
    size = 5
    df_cve_info = pd.read_csv('./output/cve_info_data.csv',encoding="gb2312")
    total_CVE = df_cve_info.loc[0].iloc[1]
    key_CVE = df_cve_info.loc[0].iloc[2]


    df_exploit_db = pd.read_csv('./output/exploit_db_data.csv',encoding="gb2312")
    total_exploit_db = df_exploit_db.loc[0].iloc[1]
    key_exploit_db = df_exploit_db.loc[0].iloc[2]


    df_hacker_news = pd.read_csv('./output/hacker_news_data.csv',encoding="gb2312")
    total_hacker_news = df_hacker_news.loc[0].iloc[1]
    key_hacker_news = df_hacker_news.loc[0].iloc[2]

    df_threat_book = pd.read_csv('./output/threat_book_data.csv',encoding="gb2312")
    total_threat_book = df_threat_book.loc[0].iloc[1]
    key_threat_book = df_threat_book.loc[0].iloc[2]

    df_anquanke = pd.read_csv('./output/An_quan_ke_data.csv',encoding="gb2312")
    total_anquanke = df_anquanke.loc[0].iloc[1]
    key_anquanke = df_anquanke.loc[0].iloc[2]

    total_vulns = [total_CVE,total_exploit_db,total_hacker_news,total_threat_book,total_anquanke]
    key_vulns = [key_CVE,key_exploit_db,key_hacker_news,key_threat_book,key_anquanke]
    #print(total_vulns,key_vulns)

    ind = np.arange(size)
    total_width = 0.9
    width = total_width / size

    fig,ax = plt.subplots()
    rects1 = ax.bar(ind, total_vulns, width, color='g')
    rects2 = ax.bar(ind + width, key_vulns, width, color='r')

    ax.set_ylabel('漏洞告警数')
    ax.set_title('今日漏洞告警分析')
    ax.set_xticks(ind + width)
    ax.set_xticklabels(('CVE', 'Exploit_db','Hacker_news','Thread_book','Anquanke'))

    ax.legend((rects1[0], rects2[0]), ('告警总数', '检索数'))
    plt.savefig(os.path.join(config.output_path, 'inspect.png'))
    #plt.show()

if __name__ == '__main__':
    get_plt_bar()