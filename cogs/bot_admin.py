
import discord
from discord.ext import commands

import helpers.templates_to_publish as templates
import config_files.ewb_bot as ewb_config

import config_files.organization as orga

import datetime, time

from discord.ext import tasks

class BotAdmin(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        self.clear_spam_log.start()
        self.clear_raid_detect.start()

    @commands.command(name="clear", aliases = ["erase"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, lines:int):
        """Nettoie la room de X messages
        Fournir le nombre de messages (X) à retirer de la room (max. 1000)
        - ema.clear 10
        """
        lines = lines + 1
        await ctx.channel.purge(limit=lines)

    @tasks.loop(seconds=ewb_config.timing_spam_detect)
    async def clear_spam_log(self):
        with open("data/temp/spam.txt", "r+") as file:
            file.truncate(0)
            # print("[ewb.BotAdmin] spam log cleared")
    
    @tasks.loop(seconds=ewb_config.timing_raid_detect)
    async def clear_raid_detect(self):
        with open("data/temp/entry.txt", "r+") as file:
            file.truncate(0)
            # print("[ewb.BotAdmin] entry log cleared")

def setup(bot):
    bot.add_cog(BotAdmin(bot))