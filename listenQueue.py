# -*- coding:utf-8 -*-
import os
import commands
import time
import sys
from tool import configTool

path = '/Users/zuston/dev/py-dev/py-1/112.23.23.34/'
path = configTool.getConfig('queue','queue_file')
while 1:
    if os.path.exists(path):
        for file in  os.listdir(path):
            (status,output) = commands.getstatusoutput('tail -n 1 %s%s'%(path,file))
            if status:
                print 'command is error'
            # 以空格符分割字符串
            outputList = output.split(' ')
            queueStatus = int(outputList[0])
            queueTime = int(outputList[1])
            # 逻辑为状态为0,即为待处理;1即为处理完成
            if queueStatus == 0:
                if int(time.time()) - queueTime > 300:
                    (shutStatus,shutOutput) = commands.getstatusoutput('ipmitool power off')
                    shutStatus = 0
                    if shutStatus:
                        print 'command is error'
                    else:
                        print 'exec the command'
                        f = open(path + file, 'a')
                        f.write('1 %d\n'%(queueTime))
                else:
                    pass
            else:
                pass

