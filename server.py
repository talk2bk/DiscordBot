#servers have lists of channels, maps of users
import discord
from user import *
class Server(object):

   #create a server object given an id. 
    def __init__(self,server):
        self.server = server #discord's server class
        self.ignored_channels = [] #the ignored channels on the server
        self.users = [] #the list of user objects

    def getCummies(self, member):
        for temp in self.users:
            if temp.member == member:
                return temp.cummies
        #only occurs in the case where the user doesnt exist
        self.users.append(Princess(member))
        return 0
        
    def giveCummies(self, member):
        for temp in self.users:
            if temp.member == member:
                cummiesMade = self.generateCummies()
                temp.cummies = temp.cummies + cummiesMade
                self.users[self.users.index(temp)] = temp #update the list
                return cummiesMade
        #this only occurs in the case where the user doesnt exist previously
        self.users.append(Princess(member))
        return 1

    def generateCummies(self):
        import random
        return random.randint(1,10)

    def clearCummies(self):
        for temp in self.users:
            temp.cummies = 0
    
    def ignoreChannel(self,channel):
        if channel in self.ignored_channels:
            self.ignored_channels.remove(channel)
            return "{0} (id:{1}) has been removed from the ignore list".format(channel.name,channel.id)
        else:
            self.ignored_channels.append(channel)
            return "{0} (id:{1}) has been added to the ignore list".format(channel.name,channel.id)

    def checkIgnore(self,channel):
        if channel in self.ignored_channels:
            return True
        return False
