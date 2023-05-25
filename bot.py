import os
import random

import discord
from dotenv import load_dotenv
from discord.ext import commands

import requests

from rand_responses import dad_joke_prefaces
from icebreakers import icebreakers

# ENV
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')
# need the bot token from the discord developer panel stored in the .env file
#

# URLs
DAD_JOKES_URL = 'https://icanhazdadjoke.com/'

# INTENTS
intents = discord.Intents.default()
intents.message_content = True

# CLIENT
bot = commands.Bot(intents=intents, command_prefix='!')
# intents states privileges that the bot has (for example getting message content)
# command_prefix determines the prefix the bot responds to (so for example typing !standup with the ! as a prefix)

# HELPERS

def parse_dad_joke(dad_joke_dict):
    preface = random.choice(dad_joke_prefaces)
    random_emoji = random.choice(["😂", "🤣", "🤪", "😝", "😆", "", "", ""])
    return f"{preface}\n`{dad_joke_dict['joke']}` {random_emoji}"

# EVENTS / COMMANDS

@bot.event
async def on_ready():
    print(f'---{bot.user.name} has connected to Discord!---')
    # the discord.utils.get allows us to work with the guild named after the guild in the .env
    # guild is another name for the server
    guild = discord.utils.get(bot.guilds, name=SERVER)
    print(f"---[Connected to {guild.name} | id: {guild.id}]---")

@bot.command(name='standup')
async def standup(ctx, arg=""):
    print(arg)
    question = random.choice(icebreakers)
    response = f"Today's question:\n`{question}`"
    await ctx.send(response)

@bot.command(name='dadjoke')
async def dadjoke(ctx, arg=""):
    headers = {"Accept": "application/json"}
    if arg == "":
        resp = requests.get("https://icanhazdadjoke.com/", headers=headers)
        dad_joke = resp.json()
        if dad_joke["status"] == 200:
            response = parse_dad_joke(dad_joke)
            await ctx.send(response)
        else:
            response = "`404: Looks like I lost my book of jokes...`"
            await ctx.send(response)
    else:
        resp = requests.get(f"https://icanhazdadjoke.com/search?term={arg}", headers=headers)
        parsed_res = resp.json()
        if parsed_res["status"] == 200:
            if parsed_res["results"]:
                rand_joke = random.choice(parsed_res["results"])
                response = parse_dad_joke(rand_joke)
                await ctx.send(response)
            else:
                response = "Sorry I couldn't think of a joke about that topic..."
                await ctx.send(response)
        else:
            response = "`404: Looks like I lost my book of jokes...`"
            await ctx.send(response)

bot.run(TOKEN)
