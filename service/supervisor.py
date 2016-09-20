import os
import re
import commands
import time
import datetime
import sys
sys.path.append('..')
from tool import emailTool
from tool import configTool

class supervisor(object):

    __pcHost = ''
    __logDir = ''
    __logSuffix = ''

    __thresholdDict = {}


    def __init__(self,pcHost,logDir,logSuffix,**threshold):
        self.__pcHost = pcHost
        self.__logSuffix = logSuffix
        self.__logDir = logDir
        self.__thresholdDict = threshold

        self.__queueDir = self.__thresholdDict['queue_list']

    def print_pcHost(self):
        print self.__pcHost

    def print_logDir(self):
        print self.__logDir

    def print_logSuffix(self):
        print self.__logSuffix


    def dataMonitor(self):
        (status,output) = commands.getstatusoutput('impitool power status')
        # if status != 0:
        #     print 'the shell act is error,please contact me'
        #     return False
        #
        # if output != 'the return is ok':
        #     return False

        (shellStatus,info) = commands.getstatusoutput('ipmitool sensor list')

        shellStatus = 0
        info = 'CPU1 Temp        | 80.00     | degrees C  | ok    | na        | na        | na        | 84.000    | 87.000    | 89.000\nCPU2 Temp        | 100.000     | degrees C  | ok    | na        | na        | na        | 84.000    | 87.000    | 89.000'

        self.dataVerify2Mail(info)
        self.joinQueueByMailListen()

        if shellStatus != 0:
            print 'the shell act is error'
            return False

        if not os.path.exists(self.__logDir):
            print 'the logDir dont exist'
            os.mkdir(self.__logDir)

        lineList = info.split('\n')
        for oneline in lineList:

            onelineSplit = oneline.split('|')

            fileName = onelineSplit[0].lstrip().rstrip().replace(' ','-').replace('/', '-')
            saveFilePath = self.__logDir + self.__pcHost + '/' + fileName + self.__logSuffix

            writeInfo = ''
            writeInfo += time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time()))

            for key,value in enumerate(onelineSplit):
                if key < 4:
                    writeInfo += '  ' + value.strip().lstrip().replace(' ','-')
                else:
                    break
            writeInfo += '\n'
            if not os.path.exists(self.__logDir + self.__pcHost):
                os.mkdir(self.__logDir + self.__pcHost)
            if os.path.exists(saveFilePath):
               f = file(saveFilePath,'a')
            else:
                f = open(saveFilePath,'w')
            # print saveFilePath

            f.write(writeInfo)
            f.close()


    def dataVerify2Mail(self,string):

        mailContent = ''

        string = string.split('\n')
        for oneline in string:
            onelineList = oneline.split('|')
            sensorName = onelineList[0].lstrip().rstrip().replace(' ','-')
            sensorData = onelineList[1].lstrip().rstrip().replace(' ','-')
            sensorStatus = onelineList[2].lstrip().rstrip().replace(' ','-')

            if sensorData == 'na' :
                mailContent += 'the '+sensorName+' is not working,please check it!!\n'

            if re.match('CPU\d{1,2}-Temp', sensorName):
                if float(sensorData) > float(self.__thresholdDict['cpu_temp_threshold']):
                    mailContent += self.__pcHost + ' now temp :' + sensorData + ' threshold temp is %r\n'%self.__thresholdDict['gpu_temp_threshold']
            elif re.match('GPU\d{1,2}-Temp', sensorName):
                if float(sensorData) > float(self.__thresholdDict['gpu_temp_threshold']):
                    mailContent += self.__pcHost + ' now temp :' + sensorData + ' threshold temp is %r\n'%self.__thresholdDict['cpu_temp_threshold']

        if not mailContent:
            print self.__pcHost + ' is very ok'
        else:
            # print self.getMailConfig()
            # sys.exit(1)
            emailTool.sendMail(self.getMailConfig()[0],self.getMailConfig()[1],self.getMailConfig()[2],self.getMailConfig()[3],mailContent)

    def joinQueueByMailListen(self):
        # currentTime = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        currentTime = int(time.time())
        # print currentTime
        # sys.exit(1)
        if not os.path.exists(self.__queueDir):
            os.mkdir(self.__queueDir)

        self.__queueFile = self.__queueDir + self.__pcHost+'.txt'
        if not os.path.exists(self.__queueFile):
            f = open(self.__queueFile,'w')
            f.write('0 {}\n'.format(currentTime))
            f.close()
        else:
            lastTime = int((self.readLastLine().split(' '))[1])
            # lastTimeArray = time.striptime(lastTime,'%Y-%m-%d %H:%M:%S')
            # currentTimeArray = time.strptime(currentTime,'%Y-%m-%d %H:%M:%S')
            # lastTimeTim = int(time.mktime(lastTimeArray))
            # currentTimetim = int(time.mktime(currentTimeArray))
            if currentTime - lastTime > 300:
                f = file(self.__queueFile, 'a')
                f.write('0 {}\n'.format(currentTime))
                f.close()
            else:
                print 'the time internal is too short'

    def readLastLine(self):
        (status,output) = commands.getstatusoutput('tail -n 1 '+self.__queueFile)
        if not status==0:
            return False
        return output.strip()


    def getMailConfig(self):
        mailConfig = configTool.getConfigSection('mail')
        from_addr = mailConfig[0][1]
        mail_pass = mailConfig[1][1]
        smtp_server = mailConfig[2][1]
        to_addr = mailConfig[3][1]

        return from_addr,mail_pass,to_addr,smtp_server




if __name__ == '__main__':
    sp = supervisor('112.23.23.31',
                    '/Users/zuston/dev/py-dev/py-1/',
                    '.log',
                    cpu_temp_threshold=50,
                    gpu_temp_threshold=50,
                    queue_list='/Users/zuston/dev/py-dev/py-1/112.23.23.34/112-23-23-34.txt')
    sp.joinQueueByMailListen()



