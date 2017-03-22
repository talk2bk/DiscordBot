import discord
import pickle
from discord.ext.commands import Bot
from discord.ext import commands

client = discord.Client()
my_bot = Bot(command_prefix="daddy!")


#save list of ignored channels
def save_ignore(ignored_channels):
    pickle.dump(ignored_channels, open("channels.info", "wb"))

#load list of ignored channels
def load_ignore():
    return pickle.load(open("channels.info", "rb"))

#new list of ignored channels
def new_ignore():
    channels = []
    return channels

#get ignored channels
def get_ignore():
    ignored_channels = []
    try:
        ignored_channels = load_ignore()
    except FileNotFoundError:
        ignored_channels = new_ignore()
    return ignored_channels

#check if ignored
def ignored(channelid):
    ignored_channels = get_ignore()
    if channelid in ignored_channels:
        return True
    else:
        return False


# Save cummies dict
def save_dict(dict_to_save):
    pickle.dump(dict_to_save, open("dict.info", "wb"))
    
# Load cummies dict
def load_dict():
    return pickle.load(open("dict.info", "rb"))

# create cummies dict
def new_dict(member):
    cummies = {}
    return cummies

#retrieve a usable dict or make one
def get_dict():
    dict_to_use = ''
    try:
        dict_to_use = load_dict()
    except FileNotFoundError:
        dict_to_use = new_dict()
    return dict_to_use

#look up a member and returns how many cummies they have
def find_in_dict(member):
    dict_to_use = get_dict()
    userExists = False
    for name,amount in dict_to_use.items():
        #if the user already exists
        if name == member:
            #returns the number of cummies
            return dict_to_use[member]

    if userExists == False:
        #user doesnt exist, put him in
        dict_to_use[member] = 0
        save_dict(dict_to_use)
        #returns the number of cummies
        return dict_to_use[member]

@my_bot.event
async def on_read():
    print("Client logged in")

#ignore a channel
@my_bot.command(pass_context=True)
async def ignore(ctx):
    channelid = ctx.message.channel.id
    ignored_channels = get_ignore()
    if channelid in ignored_channels:
        ignored_channels.remove(channelid)
        await my_bot.say("{0}(id:{1}) has been removed from the ignore list".format(ctx.message.channel.name,channelid))
    else:
        ignored_channels.append(channelid)
        await my_bot.say("{0}(id:{1}) has been added to the ignore list".format(ctx.message.channel.name,channelid))
    save_ignore(ignored_channels)

@my_bot.command(pass_context=True)
async def mycummies(ctx):
    if not ignored(ctx.message.channel.id):
        member = ctx.message.author.name
        dict_to_use = get_dict()
        await my_bot.say('{0} has {1} cummies'.format(member, find_in_dict(member)))

@my_bot.command(pass_context=True)
async def givemesomecummies(ctx):
    if not ignored(ctx.message.channel.id):
        member = ctx.message.author.name
        dict_to_use = get_dict()
        num_of_cummies = find_in_dict(member) + 1
        dict_to_use[member] = num_of_cummies
        save_dict(dict_to_use)
        await my_bot.say('{0} now has {1} cummies'.format(member, num_of_cummies))
        
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
