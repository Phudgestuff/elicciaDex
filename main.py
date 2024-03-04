import discord
from discord.ext import commands

import os
import json

with open('./token.json', 'r') as file:
    token = json.load(file)['token']

client = commands.Bot(command_prefix='pk ')

intents = discord.Intents.default()
intents.messages = True

exclude = ['getdata.py', 'func.py']

for filename in os.listdir("./cogs"):
    if filename.endswith(".py") and (filename not in exclude):
        client.load_extension(f"cogs.{filename[:-3]}")
        print('imported', filename[:-3])

@client.event
async def on_ready():
    print('logged in as', client.user)

client.run(token)
