import os


# 结果保存路径
output_path = './output'
if not os.path.exists(output_path):
    os.makedirs(output_path)

vulns_news = ['CVE_news','Exploit_db','Hacker_news','Threat_book','An_quanke']

keywords = ['WordPress','Struts','Jboss','Remote Code Execution Vulnerability','Joomla','Linux','Windows'] 