import asyncio
import pickle
import discord  #pip install pydiscord?
import random

client = discord.Client()

def nocall():
    asyncio.sleep(1)

def log(strin):
    now = datetime.now()
    fi = open("logfile.log", "at")
    fi.write(now.strftime("%Y-%m-%d %H-%M-%S,") + str(strin) + "\n")
    fi.close()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')

@client.event
async def on_message(message):
    global game
    if not message.content.startswith("!"):
        #message is not a command
        return
    elif message.author.bot:
        #message is made by a bot
        return

    elif message.content.startswith('!admin '): #runs statment and echos to where it came from
        try:
            if len(message.content) >= 7 and game.isAdmin(message.author.id):
                evalStr = eval(message.content[7:])
                if evalStr is None or len(str(evalStr)) == 0:
                    await message.channel.send("Successful.")
                else:
                    await message.channel.send(str(evalStr))
                return
        except Exception as e:
            print(repr(e))
            await message.channel.send("oops, an error occured:\n"+str(repr(e)))
            return

    elif message.content.startswith('!awaitadmin '): #runs statment and echos to where it came from
        try:
            if len(message.content) >= 11 and game.isAdmin(message.author.id):
                evalStr = await eval(message.content[11:])
                if evalStr is None or len(str(evalStr)) == 0:
                    await message.channel.send("Successful.")
                else:
                    await message.channel.send(str(evalStr))
                return
        except Exception as e:
            print(repr(e))
            await message.channel.send("oops, an error occured:\n"+str(repr(e)))
            return

    elif message.content.startswith('!exec '): #runs exec and echos to where it came from
        try:
            if len(message.content) >= 6 and game.isAdmin(message.author.id):
                exec(message.content[6:])
                await message.channel.send("Successful.")
                return
        except Exception as e:
            print(repr(e))
            await message.channel.send("oops, an error occured:\n"+str(repr(e)))
            return

    elif message.content.startswith('!adminto '):   #runs statment and echos to where the mention points
        try:
            if len(message.content) >= 9 and game.isAdmin(message.author.id):
                evalStr = eval(message.content[9:])
                if evalStr is None or len(str(evalStr)) == 0:
                    evalStr = "Successful."
                for person in message.mentions:
                    if (person.dm_channel is None):
                        await person.create_dm()
                    await person.dm_channel.send(str(evalStr))
        except Exception as e:
            print(repr(e))
            await message.channel.send("oops, an error occured:\n"+str(repr(e)))
            return

client.run(open("TOKEN", "r").read().rstrip())
