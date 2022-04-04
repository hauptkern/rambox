import configparser
CONFIG_FILE="config.ini"
class configurator:
    def readconfig(self):
        return self.config
    def writeconfig(self):
        f=open(CONFIG_FILE,"w")
        self.config.write(f)
        f.close()
    def __init__(self):
        self.config=configparser.ConfigParser()
        self.config.read(CONFIG_FILE)
