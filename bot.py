import discord
import pickle
from discord.ext.commands import Bot
from discord.ext import commands
from server import *

client = discord.Client()
my_bot = Bot(command_prefix="daddy!")
currentServer = None
'''
todo:
#it now saves servers on an id basis

'''
#ignore - list of channels on a server to ignore
#dict - map of users to cummies on a server
#server - pickle each server object containing list of channels, user objects


#save server to file
def save_server(server_to_save):
    pickle.dump(server_to_save, open(server_to_save.server.id, "wb"))
    
#load server from file
def load_server(serverid):
    return pickle.load(open(serverid, "rb"))

#create server
def new_server(server):
    tempServer = Server(server)
    return tempServer

#retrieve server to be used
def get_server(server):
    global currentServer
    if currentServer is not None:
        if currentServer == server:
            return currentServer
    try:
        currentServer = load_server(server.id)
    except FileNotFoundError:
        currentServer = new_server(server)
    return currentServer

#checks flags such as being an ignored channel or an admin only command
def check_flags(ctx, checkIgnore = False, checkAdmin = False):
    get_server(ctx.message.server)
    if checkIgnore:#if the flag to check ignore is true
        if currentServer.checkIgnore(ctx.message.channel): #if the currentserver is ignoring the channel
            return False #don't allow
    elif checkAdmin: #if this command requires admin level
        if ctx.message.author.permissions_in(ctx.message.channel).administrator == False:
            return False
    return True

#ignore a channel
@my_bot.command(pass_context=True)
async def ignore(ctx):
    #add so only admins can affect
    if check_flags(ctx,False,True):
        channel = ctx.message.channel
        await my_bot.say(get_server(ctx.message.server).ignoreChannel(channel))
        save_server(currentServer)
        
#check amount of cummies
@my_bot.command(pass_context=True)
async def mycummies(ctx):
    if check_flags(ctx, True):
        member = ctx.message.author
        await my_bot.say('{0} has {1} cummies'.format(member.nick, get_server(ctx.message.server).getCummies(member)))

'''
add messages to differing amounts of cummies received
also add a cooldown or a weight system on how many cummies you can receive
'''
#receive cummies from daddy
@my_bot.command(pass_context=True)
async def givemesomecummies(ctx):
    if check_flags(ctx,True):
        member = ctx.message.author
        cummiesGiven = get_server(ctx.message.server).giveCummies(member)
        await my_bot.say('{0} now has {1} cummies after receiving {2} cummies!'.format(member.nick,currentServer.getCummies(member), cummiesGiven))
        save_server(currentServer)

#clear cummies
'''
TO DO: ADD A DOUBLE CHECK TO THIS BEFORE IT RESOLVES
'''
@my_bot.command(pass_context=True)
async def nocummiesforanyone(ctx):
    if check_flags(ctx, True, True):
        get_server(ctx.message.server).clearCummies()
        await my_bot.say("Daddy has revoked all his princesses' cummies")
        save_server(currentServer)
        
''' to be implemented at a later date maybe
@my_bot.command(pass_context=True)
async def sharethecummies(ctx, target):
    if not ignored(ctx.message.channel.id):
        #look up the user calling
        member = ctx.message.author.name
        dict_to_use = get_dict()
        num_of_cummies = find_in_dict(member)
        #subtract a cummy
        dict_to_use[member] = num_of_cummies - 1
        #look up the target
        
        #give him a cummy
'''
my_bot.run("MjkzODgwODI0NzA3ODA5Mjkw.C7NbRg.04sHktnAAvBG6t2imj-uw01pRLA")
