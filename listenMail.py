# -*- coding:utf-8 -*-
import os
import re
import sys
import time
sys.path.append('/Users/zuston/dev/py-dev/py-1/supervisor')
from service import supervisor
from tool import configTool
from tool import emailTool
import commands
from functools import partial



path = configTool.getConfig('queue','queue_file')
count = 1
number = 0

threshold = 300

email = configTool.getConfigSection('mail')
from_addr = email[0][1]
mail_password = email[1][1]
smtp_server = email[2][1]

# print type(from_addr)
# sys.exit(1)

getmail = partial(emailTool.getMail,from_addr,mail_password,smtp_server)

while 1:
    if count == 1:
        (mail_number, mailSubject) = getmail()
        number = mail_number
    else:
        (mail_number, mailSubject) = getmail(number)
        # mailSubject = '112.23.23.34'
        if not mailSubject:
            print '没有最新邮件进入'
        else:
            if mailSubject == '112.23.23.34':
                filePath = path + mailSubject.replace('.','-') + '.txt'
                if os.path.exists(filePath):
                    (status,output) = commands.getstatusoutput('tail -n 1 %s'%filePath)
                    if not status:
                        queueStatus = (output.split(' '))[0]
                        queueTime = int((output.split(' '))[1])
                        if not int(queueStatus):
                            currentTime = int(time.time())
                            if currentTime - queueTime < threshold:
                                f = open(filePath,'a')
                                f.write('1 %d\n' % (queueTime))
                print filePath
            break
    count += 1
    time.sleep(5)
