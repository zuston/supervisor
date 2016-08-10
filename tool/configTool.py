import ConfigParser
import os

def getConfig(section,key) :
    config = ConfigParser.ConfigParser()
    # if not os.path.exists('./../config') :
    #     return False
    # if not os.path.exists('./../config/config.ini') :
    #     return False

    config.read('config/config.ini')
    return config.get(section,key)

def getConfigSection(section) :
    config = ConfigParser.RawConfigParser()
    # if not os.path.exists('./../config'):
    #     return False
    # if not os.path.exists('./../config/config.ini'):
    #     return False

    config.read('config/config.ini')
    return config.items(section)



if __name__ == "__main__" :
    print getConfig('threshold','cpu_temp_threshold')
    print getConfigSection('threshold')