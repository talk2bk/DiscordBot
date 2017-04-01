import discord
import pickle
from discord.ext.commands import Bot
from discord.ext import commands
from server import *
from botinfo import*

client = discord.Client()
my_bot = Bot(command_prefix="daddy!")
currentServer = None
euphemism = 'boy juice' #convert into a list of different phrases, then pick one at random
'''
todo:
#shang tsun randomly steals yo cummies
#making slots is prob real easy, it just speaks a few lines, each image is just an emoticon
#fix dailies AGAIN

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

#start of commands

'''
implement gambling
'''

#ignore a channel
@my_bot.command(pass_context=True,help = "Use to ignore a channel, use again to unignore.",brief = "Admin only.")
async def ignore(ctx):
    if check_flags(ctx,False,True):
        channel = ctx.message.channel
        await my_bot.say(get_server(ctx.message.server).ignoreChannel(channel))
        save_server(currentServer)
        
#check amount of cummies
@my_bot.command(pass_context=True,help = "Your cummies.")
async def mycummies(ctx):
    if check_flags(ctx, True):
        member = ctx.message.author
        await my_bot.say('{0} has {1} cummies'.format(member.display_name, get_server(ctx.message.server).getCummies(member)))

'''
add messages to differing amounts of cummies received
'''
#receive cummies from daddy
@my_bot.command(pass_context=True, help = "Get some cummies from Daddy.")
async def givemesomecummies(ctx):
    if check_flags(ctx,True):
        member = ctx.message.author
        cummiesGiven = get_server(ctx.message.server).giveCummies(member)
        if cummiesGiven > 0:
            if cummiesGiven >= Server.maxCummies:
                await my_bot.say("Ooooooh baby, you hit big Daddy's jackpot!")
            await my_bot.say('{0} now has {1} cummies after receiving {2} cummies from daddy! Daddy has {3} shots left for this little princess!'.format(member.display_name,currentServer.getCummies(member), cummiesGiven, currentServer.getDailies(member)))
        else:
            timeLeft = currentServer.timeLeft(currentServer.users[currentServer.lookup(member)])
            await my_bot.say('Daddy has to rest honey. Daddy will have more {3} in {0}H:{1}M:{2}S.'.format(timeLeft.hour,timeLeft.minute,timeLeft.second, euphemism))
        save_server(currentServer)

@my_bot.command(pass_context=True, help="Show everyone with cummies in descending order.")
async def favoriteprincess(ctx):
    if check_flags(ctx,True):
        i = 1
        result = ''
        for user in get_server(ctx.message.server).getTop():
            result += '{2}. {0} has {1} cummies! \n'.format(user.member.display_name,user.cummies,i)
            i += 1
        await my_bot.say(result)


@my_bot.command(pass_context=True, help = "Give any number of uses X cummies.", brief  = "[number of cummies] [names or @mentions]")
async def sharethecummies(ctx,num_of_cummies = 1,*targets):
    if check_flags(ctx,True):
        member = ctx.message.author
        get_server(ctx.message.server)
        if not ctx.message.mentions:
            for name in targets:
                if currentServer.donateCummiesName(ctx,member, name, num_of_cummies):
                    await my_bot.say('{0} has shared {1} cummies with {2}'.format(member.display_name, num_of_cummies, currentServer.lookupName(name).member.display_name))
                else:
                    await my_bot.say('Donation unsuccessful, not enough cummies.')
        else:
            for user in ctx.message.mentions:
                if currentServer.donateCummiesMentions(member, user, num_of_cummies):
                    await my_bot.say('{0} has shared {1} cummies with {2}'.format(member.display_name, num_of_cummies, user.display_name))
                else:
                    await my_bot.say('Donation unsuccessful, not enough cummies.')
        save_server(currentServer)

#idunnowaht this should even do
@my_bot.command(pass_context=True,hidden = True)
async def cummiesareyummy(ctx):
    await my_bot.say('doesnt do nothin yet')

#gamblin method
@my_bot.command(pass_context=True)
async def bigcummies(ctx,num_of_cummies = 1,gambleType = 'doubleOrNothing'):
    if check_flags(ctx,True):
        member = ctx.message.author
        winnings = get_server(ctx.message.server).gambleCummies(member, num_of_cummies, gambleType)
        if winnings <= 0:
            await my_bot.say('{0} has bet {1} cummies and gotten cucked. NO CUMMIES.'.format(member.display_name,num_of_cummies))
        else:
            if winnings > 500:
                await my_bot.say("{0} has bet {1} cummies and made BIG CUMMIES. {2} CUMMIES. NOW THAT'S SOME BIG CUMMIES".format(member.display_name, num_of_cummies, winnings))
            else:
                await my_bot.say('{0} has bet {1} cummies and made BIG CUMMIES. {2} CUMMIES.'.format(member.display_name, num_of_cummies,winnings))
        save_server(currentServer)

@my_bot.command(pass_context=True,hidden=True)
async def updateUsers(ctx):
    get_server(ctx.message.server).updateUserObjects()
    save_server(currentServer)
'''
TO DO: ADD A DOUBLE CHECK TO THIS BEFORE IT RESOLVES
this command seems unnecessary anyway
#clear cummies
@my_bot.command(pass_context=True)
async def nocummiesforanyone(ctx):
    if check_flags(ctx, True, True):
        await my_bot.say("are you sure?")
        response = await client.wait_for_message(author = ctx.message.author,channel = ctx.message.channel)
        if response.content.startswith('y'):
            get_server(ctx.message.server).clearCummies()
            await my_bot.say("Daddy has revoked all his princesses' cummies")
            save_server(currentServer)
'''



my_bot.run(serverInfo().toString())
