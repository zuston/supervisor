# -*- coding:utf-8 -*-
import poplib
from email import encoders
from email.header import Header,decode_header
from email.mime.text import MIMEText
from email.parser import Parser
from email.utils import parseaddr, formataddr
import smtplib
import email
import time
import sys



def _format_addr(s):
    name, addr = parseaddr(s)
    return formataddr((Header(name, 'utf-8').encode(), addr))

def sendMail(from_addr,password,to_addr,smtp_server,mail_info) :
    msg = MIMEText(mail_info, 'plain', 'utf-8')
    msg['From'] = _format_addr('supervisor manager <%s>' % from_addr)
    msg['To'] = _format_addr('manager <%s>' % to_addr)
    msg['Subject'] = Header('important notice!!!', 'utf-8').encode()
    server = smtplib.SMTP(smtp_server, 25)
    # server.set_debuglevel(1)
    server.login(from_addr, password)
    server.sendmail(from_addr, [to_addr], msg.as_string())
    server.quit()


def getMail(from_addr,password,pop3_server,mail_number=0) :
    server = poplib.POP3(pop3_server)
    # 错误日志
    # server.set_debuglevel(1)
    print server.getwelcome()
    # sys.exit(1)
    # 身份认证
    server.user(from_addr)
    server.pass_(password)

    # print 'Message:%s || Size:%s'%server.stat()
    resp,mails,number = server.list()
    # 获取最新一封邮件
    index = len(mails)
    if index>mail_number:
        resp, lines, octets = server.retr(index)
        server.quit()
        lines = '\r\n'.join(lines)
        msg = Parser().parsestr(lines)
        return index, print_info(msg)
    else :
        server.quit()
        return mail_number,''


def print_info(msg, indent=0):
    subject = ''
    if indent == 0:
        # 邮件的From, To, Subject存在于根对象上:
        for header in ['From', 'To', 'Subject']:
            value = msg.get(header, '')
            if value:
                if header=='Subject':
                    # 需要解码Subject字符串:
                    value = decode_str(value)
                    subject = value
                else:
                    # 需要解码Email地址:
                    hdr, addr = parseaddr(value)
                    name = decode_str(hdr)
                    value = u'%s <%s>' % (name, addr)
            # print('%s%s: %s' % ('  ' * indent, header, value))

    if (msg.is_multipart()):
        # 如果邮件对象是一个MIMEMultipart,
        # get_payload()返回list，包含所有的子对象:
        parts = msg.get_payload()
        for n, part in enumerate(parts):
            # print('%spart %s' % ('  ' * indent, n))
            # print('%s--------------------' % ('  ' * indent))
            # 递归打印每一个子对象:
            print_info(part, indent + 1)
    else:
        # 邮件对象不是一个MIMEMultipart,
        # 就根据content_type判断:
        content_type = msg.get_content_type()
        if content_type=='text/plain' or content_type=='text/html':
            # 纯文本或HTML内容:
            content = msg.get_payload(decode=True)
            # 要检测文本编码:
            charset = guess_charset(msg)
            if charset:
                content = content.decode(charset)
            # print('%sText: %s' % ('  ' * indent, content + '...'))
        else:
            pass
            # print('%sAttachment: %s' % ('  ' * indent, content_type))
    return subject

def decode_str(s):
    value, charset = decode_header(s)[0]
    if charset:
        value = value.decode(charset)
    return value

def guess_charset(msg):
    # 先从msg对象获取编码:
    charset = msg.get_charset()
    if charset is None:
        # 如果获取不到，再从Content-Type字段获取:
        content_type = msg.get('Content-Type', '').lower()
        pos = content_type.find('charset=')
        if pos >= 0:
            charset = content_type[pos + 8:].strip()
    return charset


if __name__ == '__main__':
    sys.path.append('/Users/zuston/dev/py-dev/py-1/supervisor')
    from tool import configTool
    from functools import partial

    email = configTool.getConfigSection('mail')
    from_addr = email[0][1]
    mail_password = email[1][1]
    pop_server = email[4][1]

    print from_addr
    print mail_password
    print pop_server
    # sys.exit(1)

    sendMail(from_addr,mail_password,'731673917@qq.com','smtp.sina.cn','hello')
    sys.exit(1)

    gM = partial(getMail,from_addr,mail_password,pop_server)

    count = 1
    number = 0
    while 1:
        if count==1:
            (mail_number, mailSubject) = gM()
            number = mail_number
        else:
            (mail_number, mailSubject) = gM(number)
            if not mailSubject:
                print '没有最新邮件进入'
            else:
                print mailSubject
                break
        count += 1
        time.sleep(10)




