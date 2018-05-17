import cve_info
import exploit_db
import hacker_news
import threat_book
import anquanke
import smtplib
import make_chart
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders
from email.header import Header


def send_email_with_pic(mail_msg):
    sender = 'xxx@xx.com' # 发件人
    password = 'xxx' # 发件人密码
    receiver = 'xxx@qq.com' # 收件人
    message = MIMEMultipart('alternative') 
    message['From'] = sender
    message['To'] = receiver
    subject = '最新漏洞和CVE告警信息'
    message['Subject'] = Header(subject, 'utf-8')
    message.attach(MIMEText(mail_msg, 'html', 'utf-8'))
    with open('./output/inspect.png','rb') as f:
        mm = MIMEBase('image', 'png', filename='inspect.png')
        mm.add_header('Content-Disposition', 'attachment', filename='inspect.png')
        mm.add_header('Content-ID', '<0>')
        mm.add_header('X-Attachment-Id', '0')
        mm.set_payload(f.read())
        encoders.encode_base64(mm)
        message.attach(mm)

    try:
        smtpObj = smtplib.SMTP('smtp.163.com')
        smtpObj.login(sender, password)
        smtpObj.sendmail(sender, receiver, message.as_string())
        print('邮件发送成功')
    except smtplib.SMTPException:
        print('Error: 无法发送邮件')


def main():
    CVE_info_msg = cve_info.get_CVE_info()
    exploit_db_msg = exploit_db.get_exploit_db_info()
    hacker_news_msg = hacker_news.get_hacker_news_info()
    threat_book_msg = threat_book.get_threat_book_info()
    Anquanke_msg = anquanke.get_anquanke_info()
    total_msg = CVE_info_msg + exploit_db_msg + hacker_news_msg + threat_book_msg + Anquanke_msg
    make_chart.get_plt_bar()
    send_email_with_pic(total_msg)


if __name__ == '__main__':
    main()
    

