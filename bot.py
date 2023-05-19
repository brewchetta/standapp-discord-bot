import os
import random

import discord
from dotenv import load_dotenv

import requests

from rand_responses import dad_joke_prefaces
from icebreakers import icebreakers

# ENV
load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')
SERVER = os.getenv('DISCORD_SERVER')

# URLs
DAD_JOKES_URL = 'https://icanhazdadjoke.com/'

# INTENTS
intents = discord.Intents.default()
intents.message_content = True

# CLIENT
client = discord.Client(intents=intents)

# EVENTS

@client.event
async def on_ready():
    print(f'---{client.user} has connected to Discord!---')
    # the discord.utils.get allows us to work with the guild named after the guild in the .env
    # guild is another name for the server
    guild = discord.utils.get(client.guilds, name=SERVER)
    print(f"---[Connected to {guild.name} | id: {guild.id}]---")
    # print(f"\nCurrent Members:")
    # for member in guild.members:
    #     print(f"--> {member.name}")

@client.event
async def on_message(message):
    # print(f'---[New Message: "{message.content}"]---')

    # the two lines below allow the bot to ignore its own messages
    if message.author == client.user:
        return

    if message.content == '!standup':
        question = random.choice(icebreakers)
        response = f"Today's question:\n{question}"
        await message.channel.send(response)

    if message.content == '!dadjoke':
        headers = {"Accept": "application/json"}
        resp = requests.get("https://icanhazdadjoke.com/", headers=headers)
        dad_joke = resp.json()
        if dad_joke["status"] == 200:
            preface = random.choice(dad_joke_prefaces)
            response = f"{preface}\n{dad_joke['joke']}"
            await message.channel.send(response)
        else:
            response = "That didn't quite work..."
            await message.channel.send(response)


client.run(TOKEN)
