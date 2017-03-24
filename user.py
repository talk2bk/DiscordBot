import discord
class Princess(object):
    #add a datetime
    def __init__(self,member, num_of_cummies=0):
        self.member = member #save the member class information from discord
        self.cummies = num_of_cummies

    def __cmp__(self, other):
        if self.cummies < other.cummies:
            return -1
        elif self.cummies > other.cummies:
            return 1
        return 0


    #doesnt work - figure out why    
    def add_cummies(self, num_of_cummies = 1):
        self.cummies += num_of_cummies
        
    def remove_cummies(self,num_of_cummies = 1):
        self.cummies -= num_of_cummies

    
