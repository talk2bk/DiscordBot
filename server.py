#servers have lists of channels, maps of users
import discord
from user import *
class Server(object):

   #create a server object given a server.
    def __init__(self,server):
        self.server = server #discord's server class
        self.ignored_channels = [] #the ignored channels on the server
        self.users = [] #the list of user objects

    def getCummies(self, member):
        for temp in self.users:
            if temp.member == member:
                return temp.cummies
        #only occurs in the case where the user doesnt exist
        self.createNewUser(member,0)
        return 0
        
    def giveCummies(self, member):
        for temp in self.users:
            if temp.member == member:
                cummiesMade = self.generateCummies() #make cummies
                temp.cummies = temp.cummies + cummiesMade #add cummies to the user
                self.users[self.users.index(temp)] = temp #update the list
                return cummiesMade
        #this only occurs in the case where the user doesnt exist previously
        self.createNewUser(member,1)
        return 1

    def donateCummiesMentions(self, donater, target, num_of_cummies):
        index = self.lookup(donater)
        temp = self.users[index]
        if temp.cummies >= num_of_cummies:
            temp.remove_cummies(num_of_cummies)
            self.users[index] = temp
            targetindex = self.lookup(target)
            targetTemp = self.users[targetindex]
            targetTemp.add_cummies(num_of_cummies)
            self.users[targetindex] = targetTemp
            return True
        else:
            return False

    def donateCummiesName(self,ctx,donater, target, num_of_cummies):
        currentServerMembers = ctx.message.server.members
        for member in currentServerMembers:
            if target.upper() in member.name.upper() or target.upper() in member.display_name.upper():
                return self.donateCummiesMentions(donater,member,num_of_cummies)
        return False

    def lookupName(self,name):
        for temp in self.users:
            if name.upper() in temp.member.name.upper() or name.upper() in temp.member.display_name.upper():
                return temp

    def lookup(self, member):
        for temp in self.users:
            if temp.member == member:
                return self.users.index(temp) #if the user exists, return where he is
        #only occurs if user didnt exist during lookup
        self.createNewUser(member,0) #create a new user with no cummies
        return len(self.users)-1 #return the last index

    def createNewUser(self,member,num_of_cummies=0):
        self.users.append(Princess(member,num_of_cummies))

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

    def getTop(self):
        return sorted(self.users, key = lambda princess: princess.cummies, reverse = True)