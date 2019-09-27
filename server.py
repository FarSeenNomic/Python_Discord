import asyncio
import pickle
import discord  #pip install pydiscord?
import random
from datetime import datetime

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
    if not message.content.startswith("!"):
        #message is not a command
        return
    elif message.author.bot:
        #message is made by a bot
        return

    elif message.content.startswith('!admin '): #runs statment and echos to where it came from
        try:
            if len(message.content) >= 7 and message.author.id == 269904594526666754:
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
            if len(message.content) >= 11 and message.author.id == 269904594526666754:
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
            if len(message.content) >= 6 and message.author.id == 269904594526666754:
                exec(message.content[6:])
                await message.channel.send("Successful.")
                return
        except Exception as e:
            print(repr(e))
            await message.channel.send("oops, an error occured:\n"+str(repr(e)))
            return

    elif message.content.startswith('!adminto '):   #runs statment and echos to where the mention points
        try:
            if len(message.content) >= 9 and message.author.id == 269904594526666754:
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

    if message.content.startswith('!vote') and message.author.id == 269904594526666754:
        # get a dict with all people
        peo = {i.id : None for i in message.guild.members if not i.bot}
        await message.channel.send("say `!yea` to vote yes\nsay `!nay` to vote no")

        def ch():
            return "Yea: " + ", ".join(i for i in peo if i is True) + "\nNay: " + ", ".join(i for i in peo if i is False) + "\nNoV: " + ", ".join(i for i in peo if i is None)

        randomOptOut = random.randint(10000,99999)
        print(randomOptOut)

        def check(m):
            #if "end", end
            #if "check", send
            #if "yea"
            #if "nay"
            #if everyone, return
            if m.content.startswith("!end") and m.author.id == 269904594526666754:
                return True
                
            elif m.content.startswith("!"+(randomOptOut-1)) or m.content.startswith("!"+(randomOptOut+1)):
                await message.channel.send("OBOE")
                randomOptOut = random.randint(10000,99999)
                return False

            elif m.content.startswith("!"+randomOptOut):
                peo.pop(m.author.id)
                randomOptOut = random.randint(10000,99999)
                return False

            elif m.content.startswith("!check"):
                await message.channel.send(ch())
                return False

            elif m.content.startswith("!yea"):
                peo[m.author.id] = True
                await message.channel.send(m.display_name + " voted yea")
                return False

            elif m.content.startswith("!nay"):
                peo[m.author.id] = False
                await message.channel.send(m.display_name + " voted nay")
                return False

            return len([i for i in peo if i is None]) == 0

        await client.wait_for('message', check=check, timeout=60*60*24)
        await message.channel.send("final:\n" + ch())

client.run(open("TOKEN", "r").read().rstrip())
