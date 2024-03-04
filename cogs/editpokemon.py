import discord
from discord.ext import commands

from main import client
from cogs.getdata import pokemon as pokemonDB

add = client.create_group('add', 'Search for stuff')

class editing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @add.command()
    async def pokemon(ctx, name, type, hp, attack, defense, specialattack, specialdefense, speed):
        pass

def setup(client):
    client.add_cog(editing(client))