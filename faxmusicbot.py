import discord
from discord.ext import commands
from discord.ext import tasks
import pafy
from asyncio import sleep
import ffmpeg

bot = discord.ext.commands.Bot(command_prefix = "m")
urlist = []
timelist = []
pos = 0
lastpos = 0
current_time = 1000
ctxForAll = 0
hasJoined = 0
timer = 0
skip = False
is_paused = False
firstTime = True

#----------------------------------------------------------
#     #Events, taskloops, and sound definition.
#----------------------------------------------------------

@bot.event
async def on_ready():
    channel = bot.get_channel(801885908261142549)
    await channel.send("Bot started! This is intended only for ℻ Clan use. Made by TresTilo#4307")

@tasks.loop(seconds=2)
async def playNext():
    global is_paused
    global timer
    if not is_paused:
        timer += 2
    make_sound()
    
def make_sound():
    global lastpos
    global pos
    global ctxForAll
    global current_time
    global timer
    global skip
    global firstTime
    global urlist
    if ctxForAll == 0:
        return
    if firstTime:
        firstTime = False
        playNext.start()
    else:
        if (timer >= current_time and len(urlist)-1 >= pos) or skip:
            skip = False                
            ctxForAll.voice_client.stop()
            vc = ctxForAll.voice_client
            timer = -1
            current_time = timelist[pos]
            vc.play(discord.FFmpegOpusAudio(source=urlist[pos]))
            lastpos = pos
            pos = pos + 1

#----------------------------------------------------------
#     #Bot commands:
#----------------------------------------------------------

@bot.command()
async def stop(ctx):
    global urlist
    global pos
    global lastpos
    global current_time
    global ctxForAll
    global hasJoined
    global timelist
    timelist = []
    hasJoined = 0
    urlist = []
    pos = 0
    lastpos = 0
    current_time = 0
    ctxForAll = 0
    await ctx.voice_client.disconnect()

@bot.command()
async def discordbot(ctx):
    if ctx.author == bot.user:
        return
    elif str(ctx.author) == "TresTilo#4307":
        await ctx.channel.send("The ℻ Clan music bot is one of many upcoming projects, like a cryptocurrency\n"
                                   +"Feel free to contact us for any inquiries.")
    else:
        await ctx.channel.send("You are not allowed to use this command!")

@bot.command()
async def skip(ctx):
    global skip
    global urlist
    global pos
    try:
        urlist = urlist[pos:]
        pos = 0
        urlist[0]
    except:
        await ctx.send("There is nothing to skip!")
    else:
        global is_paused
        is_paused = False #It might be paused and skipped at the same time.
        skip = True
        make_sound()


@bot.command()
async def play(ctx,url):
    global hasJoined
    global timelist
    
    if hasJoined == 0:
        global ctxForAll
        ctxForAll = ctx
        if ctx.author.voice is None:
            await ctx.send("You are not in a voice channel!")
        voice_channel = ctx.author.voice.channel
        if ctx.voice_client is None:
            hasJoined = 1
            video = pafy.new(url)
            duration = video.length
            best = video.getbestaudio()
            playurl = best.url
            urlist.append(playurl)
            timelist.append(duration)
            await voice_channel.connect()
            make_sound()
        else:
            await ctx.voice_client.move_to(voice_channel)
    else:
        video = pafy.new(url)
        duration = video.length
        best = video.getbestaudio()
        playurl = best.url
        urlist.append(playurl)
        timelist.append(duration)


@bot.command()
async def projects(ctx):
    await ctx.channel.send("A cryptocurrency is on the works. More information about it will be released once the project is advanced")
    
@bot.command()
async def creator(ctx):
    await ctx.channel.send("TresTilo#4307")
    
@bot.command()
async def botinfo(ctx):
    await ctx.channel.send("The bot isn't for public use, nor is it allowed.")
    
@bot.command()
async def pause(ctx):
    global ctxForAll
    global is_paused
    is_paused = True
    ctxForAll.voice_client.pause()
    await ctxForAll.send("Paused ⏸")

@bot.command()
async def unpause(ctx):
    global ctxForAll
    global is_paused
    is_paused = False
    ctxForAll.voice_client.resume()
    await ctxForAll.send("Unpaused ⏯")

@bot.command()
async def rules(ctx):
    global ctxForAll
    await ctxForAll.send("ONLY COMMANDS IN THIS CHAT!. This command does not exist. I know this message might be annoying, but you are NOT supposed to talk here!")
            
bot.run("OTAxNDUyMTUyNjEyOTgyODU0.YXQEvQ.VMLruGG8YB80co0zuc__1tXmF1w")
