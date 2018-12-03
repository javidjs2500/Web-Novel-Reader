# Work with Python 3.6
import random
import asyncio
import aiohttp
import json
from discord import Game
from discord.ext.commands import Bot
from discord import ChannelType
from bs4 import BeautifulSoup


BOT_PREFIX = ("?", "!", "pls ")
TOKEN = 'NTE3ODgzMjA0NDgxNTgxMDYw.DuIsLA.61SIijbhN9Uxw8SpBR9HbeZAgAI'
TIME_INTERVAL = 5
client = Bot(command_prefix=BOT_PREFIX)

@client.command(name='8ball',
                description="Answers a yes/no question.",
                brief="Answers from the beyond.",
                aliases=['eight_ball', 'eightball', '8-ball'],
                pass_context=True)
async def eight_ball(context):
    possible_responses = [
        'That is a resounding no',
        'It is not looking likely',
        'Too hard to tell',
        'It is quite possible',
        'Definitely',
    ]
    await client.say(random.choice(possible_responses) + ", " + context.message.author.mention)


@client.command()
async def square(number):
    squared_value = int(number) * int(number)
    await client.say(str(number) + " squared is " + str(squared_value))


@client.event
async def on_ready():
    await client.change_presence(game=Game(name="with humans"))
    print("Logged in as " + client.user.name)


@client.command()
async def bitcoin():
    url = 'https://api.coindesk.com/v1/bpi/currentprice/BTC.json'
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        response = json.loads(response)
        await client.say("Bitcoin price is: $" + response['bpi']['USD']['rate'])

@client.command(pass_context = True)
@asyncio.coroutine
async def read(ctx, url, interval = 10):
    try:
        read.interval = int(interval)
        if interval < 0:
            raise Exception
    except:
        await client.say("The interval must be a valid integer greater than 0. The interval has defaulted to 10 seconds. You can changed this by invoking the set_interval command.")
        read.interval = 10
    read.paused = False
    read.stopped = False
    print(url)
    print(interval)
    
    @client.command()
    async def pause():
        await client.say("Reading has been paused")
        read.paused = True
    @client.command()
    async def stop():
        await client.say("Reading has stopped")
        read.stopped = True
    @client.command()
    async def resume():
        await client.say("Reading has been resumed")
        read.paused = False
    @client.command()
    async def set_interval(time):
        try:
            if int(time) < 0:
                raise Exception
            else:
                read.interval= int(time)

        except Exception:
            await client.say("The time has to be a valid integer > 0!!!")
        else:
            await client.say("The time interval has been set to " + time + "!")

    if (ctx.message.channel.type != ChannelType.private):
        await client.say("Sorry, this command cannot be used here. Please message me privately!")
    else:
        await client.say("Let's start!")
    # try:
    async with aiohttp.ClientSession() as session:  # Async HTTP request
        raw_response = await session.get(url)
        response = await raw_response.text()
        #response = json.loads(response)

        print(response)
        soup = BeautifulSoup(response, features="html.parser")
        print(soup.encode("utf-8"))

        # kill all script and style elements
        for a in soup.findAll('a'):
            a.decompose

        for script in soup(["script", "style", "navbar"]):
            script.extract()    # rip it out

        # get text
        text = soup.get_text()
        #print(text)
        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)

        #print(text)
        #print(response)

    for i in text.split("\n"):
        if read.stopped:
            return
        while read.paused:
            await asyncio.sleep(1)
        await client.say(str(i))
        await asyncio.sleep(read.interval)
    # except ValueError:
    #     await client.say("Please enter in a valid URL!")


async def list_servers():
    await client.wait_until_ready()
    while not client.is_closed:
        print("Current servers:")
        for server in client.servers:
            print(server.name)
        await asyncio.sleep(600)


client.loop.create_task(list_servers())
client.run(TOKEN)
