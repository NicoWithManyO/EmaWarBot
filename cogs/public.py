
import discord
from discord.ext import commands
from discord.ext import tasks

import config_files.emojis as emojis

import helpers.templates_to_publish as templates

# bot = discord.Bot()

class Public(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb


def setup(bot):
    bot.add_cog(Public(bot))
