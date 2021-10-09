

import discord
from discord.ext import commands
from discord.ext import tasks



class Public(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    

def setup(bot):
    bot.add_cog(Public(bot))