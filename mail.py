#!/usr/bin/env python3

from email.mime.text import MIMEText
from email.header import Header
from email.utils import parseaddr, formataddr
import smtplib

from_addr = '125003639@qq.com'
password = 'zbsosdkorlnnbhgb'
to_addr = 'ligenhw@outlook.com'
smtp_server = 'smtp.qq.com'

def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def mail():
    msg = MIMEText('hello, send by python...', 'plain', 'utf-8')
    msg['From'] = _format_addr('gen <%s>' % from_addr)
    msg['To'] = _format_addr('%s <%s>' % (to_addr,to_addr))
    msg['Subject'] = Header('来自SMTP的问候……', 'utf-8').encode()
    server = smtplib.SMTP_SSL(smtp_server, 465)
    server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    print('send mail ... quite')

if __name__ == '__main__':
    try:
        mail()
        print('Success...')
    except smtplib.SMTPException:
        print('Failed!')
