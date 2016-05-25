#-*-coding:utf8-*-
import ConfigParser
import os,sys

class configReader(object):
    def __init__(self, configPath):
        configFile = configPath
        self.cReader = ConfigParser.ConfigParser()
        self.cReader.read(configFile)

    def readConfig(self, section, item):
        return self.cReader.get(section, item)

    def getDict(self, section):
        commandDict = {}
        items = self.cReader.items(section)
        for key, value in items:
            commandDict[key] = value
        return commandDict
