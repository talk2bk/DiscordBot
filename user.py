import discord
import datetime

class Princess(object):
    def __init__(self,member, num_of_cummies=0,dailies = 2):
        self.member = member #save the member class information from discord
        self.cummies = num_of_cummies
        self.dailies = dailies
        self.lastShotUsed = datetime.datetime.today()

    def __cmp__(self, other):
        if self.cummies < other.cummies:
            return -1
        elif self.cummies > other.cummies:
            return 1
        return 0

    def getCummies(self):
        return self.cummies

    def getDailies(self):
        return self.dailies

    def incDaily(self):
        self.dailies += 1

    def decDaily(self):
        self.dailies -=1
        if self.dailies <= 0:
            self.lastShotUsed = datetime.datetime.today()

    def resetDaily(self):
        self.lastShotUsed = datetime.datetime.today()
        self.dailies = 2

    #doesnt work - figure out why    
    def add_cummies(self, num_of_cummies = 1):
        self.cummies += num_of_cummies
        
    def remove_cummies(self,num_of_cummies = 1):
        self.cummies -= num_of_cummies

    def updatedCopy(self,member, numCummies):
        return Princess(member,numCummies)
    
