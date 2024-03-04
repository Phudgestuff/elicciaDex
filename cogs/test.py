import discord
from discord.ext import commands

class testing(commands.Cog):

    def __init__(self, client):
        self.client = client

    @commands.slash_command()
    async def testrep(self, ctx):
        print('testrep')
        await ctx.respond('testing, testing, 1, 2, 3')

def setup(client):
    client.add_cog(testing(client))