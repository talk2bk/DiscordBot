import discord
class Princess(object):
    #add a datetime
    def __init__(self,member):
        self.member = member #save the member class information from discord
        self.cummies = 0

    #doesnt work - figure out why    
    def add_cummies(self):
        print('im being called')
        self.cummies = self.cummies+1
        
    def remove_cummies(self):
        self.cummies = self.cummies-1

    
