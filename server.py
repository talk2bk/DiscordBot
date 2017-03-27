#servers have lists of channels, maps of users
import discord
from user import *
import datetime
class Server(object):
    minCummies = 10
    maxCummies = 20
   #create a server object given a server.
    def __init__(self,server):
        self.server = server #discord's server class
        self.ignored_channels = [] #the ignored channels on the server
        self.users = [] #the list of user objects

    def updateUserObjects(self):
        updatedUsers = []
        for dude in self.users:
            updatedUsers.append(dude.updatedCopy(dude.member,dude.getCummies()))
        self.users = updatedUsers

    def getCummies(self,member):
        return self.users[self.lookup(member)].getCummies()
    def getDailies(self,member):
        return self.users[self.lookup(member)].getDailies()

    def giveCummies(self,member):
        userIndex = self.lookup(member)
        user = self.users[userIndex]
        if (self.checkForReset(user).days >= 1):
            user.resetDaily()
        if user.getDailies() > 0:
            cummiesMade = self.generateCummies()
            user.add_cummies(cummiesMade)
            user.decDaily()
            self.users[userIndex] = user
            return cummiesMade
        else:
            return 0 #reached daily cummy limit

    def checkForReset(self,princess):
        return princess.lastShotUsed - datetime.datetime.today()

    def timeLeft(self,princess):
        secondsLeft = self.checkForReset(princess).seconds
        secondsToReset = int(secondsLeft%60)
        minutesToReset = int((secondsLeft%3600)/60)
        hoursToReset = int((secondsLeft/3600))
        return datetime.time(hour = hoursToReset,minute = minutesToReset,second = secondsToReset)


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
        return random.randint(self.minCummies,self.maxCummies)

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

    #take away cummies, then spin the wheel. gamblecummies returns the number of cummies won.
    def gambleCummies(self,member,num_of_cummies,gambleType):
        if num_of_cummies <= self.getCummies(member):
            userIndex = self.lookup(member)
            self.users[userIndex].cummies -= num_of_cummies
            winnings = 0
            if gambleType == 'spinSlot':
                winnings = num_of_cummies * self.spinSlot()
            elif gambleType == 'rollDice':
                winnings = num_of_cummies * self.rollDice()
            else:
                winnings = num_of_cummies * self.doubleOrNothing()
            self.users[userIndex].add_cummies(winnings)
            return winnings

    #spinSlot returns a multiplier to use based on the rolls rather than anything else.
    def spinSlot(self):
        return

    #rollDice, bot rolls a dice and you roll a dice, whoever wins gets money can roll vs house or another person
    def rollDice(self):
        return

    #double or nothing
    def doubleOrNothing(self):
        import random
        if random.randint(0, 1) < 1:
            return 0
        else:
            return 2
