# coding: utf-8
import smtplib  
from email.mime.text import MIMEText  
from email.mime.multipart import MIMEMultipart
from email.mime.base import MIMEBase
from email import encoders

G_CONF = {
    'server': "smtp.ym.163.com",
    'user': "",
    'password': "",
}

class MailClient:
    def __init__(self, conf=None):
        if not conf:
            conf =  G_CONF
        self._conf = conf

    def _addExcelFile(self, data, filename):
        ctype, encoding = ('application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', None)
        maintype, subtype = ctype.split("/", 1)

        attachment = MIMEBase(maintype, subtype)
        attachment.set_payload(data)
        encoders.encode_base64(attachment)
        attachment.add_header("Content-Disposition", "attachment", filename=filename + '.xlsx')
        return attachment


    def sendMail(self, content, title, filedatas=[], to='wenjiezheng89@163.com'):
        #使用MIMEText构造符合smtp协议的header及body  
        msg = MIMEMultipart('alternative')
        msg["Subject"] = title
        msg["From"] = self._conf['user']
        if isinstance(to, list):
            to_str = ';'.join(to)
        else:
            to_str = to
        msg["To"] = to_str 

        part = MIMEText(content, 'html')
        msg.attach(part)

        for filename, filedata in filedatas:
            attachment = self._addExcelFile(filedata, filename)
            msg.attach(attachment)

        s = smtplib.SMTP(self._conf['server'], timeout=30)#连接smtp邮件服务器,端口默认是25  
        s.starttls()
        s.login(self._conf['user'], self._conf['password'])#登陆服务器  
        s.sendmail(self._conf['user'], to, msg.as_string())#发送邮件  
        s.close() 
        

if __name__ == '__main__':
    mail = MailClient()
    mail.sendMail('test', 'test', to=[])
    
