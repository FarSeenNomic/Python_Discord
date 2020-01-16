import asyncio
import discord
import random
import re
from datetime import datetime

client = discord.Client()

@client.event
async def on_ready():
    print('Logged in as')
    print(client.user.name)
    print('------')

async def adminQ(author):
    if author.id == 269904594526666754:
        return True
    if await author.guild.get_role(666763053060063263) in author.roles:
        return True
    return False
    
@client.event
async def on_message(message):
    if not message.content.lower().startswith("!"):
        #message is not a command
        return
    elif message.author.bot:
        #message is made by a bot
        return

    elif message.content.lower().startswith('!admin '): #runs statment and echos to where it came from
        try:
            if len(message.content) >= 7 and await adminQ(message.author):
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

    elif message.content.lower().startswith('!awaitadmin '): #runs statment and echos to where it came from
        try:
            if len(message.content) >= 11 and await adminQ(message.author):
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

    elif message.content.lower().startswith('!exec '): #runs exec and echos to where it came from
        try:
            if len(message.content) >= 6 and await adminQ(message.author):
                exec(message.content[6:])
                await message.channel.send("Successful.")
                return
        except Exception as e:
            print(repr(e))
            await message.channel.send("oops, an error occured:\n"+str(repr(e)))
            return

    elif message.content.lower().startswith('!adminto '):   #runs statment and echos to where the mention points
        try:
            if len(message.content) >= 9 and await adminQ(message.author):
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

    if message.content.lower().startswith('!vote') and await adminQ(message.author):
        # get a dict with all people
        peo = {}
        if message.role_mentions:
            peo = {i.id : None for i in message.role_mentions[0].members if not i.bot}
        else:
            peo = {i.id : None for i in message.guild.members if not i.bot}
        await message.channel.send("say `!yea` to vote yes\nsay `!nay` to vote no")

        def ch():
            return "Yea: " + ", ".join(str(i) for i,b in peo.items() if b is True) + "\nNay: " + ", ".join(str(i) for i,b in peo.items() if b is False) + "\nNoV: " + ", ".join(str(i) for i,b in peo.items() if b is None)

        def cnt():
            return "Yea: " + str(len([i for i in list(peo.values()) if i is True])) + "\nNay: " + str(len([i for i in list(peo.values()) if i is False])) + "\nNoV: " + str(len([i for i in list(peo.values()) if i is None]))

        randomOptOut = random.randint(10000,99999)
        print(randomOptOut)

        async def check(m):
            nonlocal peo
            nonlocal randomOptOut
            #if "end", end
            #if "check", send
            #if "yea"
            #if "nay"
            #if everyone, return

            if m.channel != message.channel:
                return

            if m.content.lower().startswith("!end") and await adminQ(m.author.id):
                return True

            elif m.content.startswith("!"+str(randomOptOut-1)) or m.content.startswith("!"+str(randomOptOut+1)):
                randomOptOut = random.randint(10000,99999)
                print(randomOptOut)
                return False

            elif m.content.startswith("!"+str(randomOptOut)):
                for p in m.mentions:
                    peo.pop(p.id)
                randomOptOut = random.randint(10000,99999)
                print(randomOptOut)
                return False

            elif m.content.lower().startswith("!check"):
                await m.channel.send(ch())
                return False

            elif m.content.lower().startswith("!count"):
                await m.channel.send(cnt())
                return False

            elif m.content.lower().startswith("!yea"):
                peo[m.author.id] = True
                await m.channel.send(m.author.display_name + " voted yea")
                return False

            elif m.content.lower().startswith("!nay"):
                peo[m.author.id] = False
                await m.channel.send(m.author.display_name + " voted nay")
                return False

            return len([i for i in list(peo.values()) if i is None]) == 0

        while True:
            if(await check(await client.wait_for('message'))):
                break

        await message.channel.send("final:\n" + ch())

client.run(open("TOKEN", "r").read().rstrip())
