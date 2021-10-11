
from discord.ext import commands

import discord

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
        """Nettoie la room"""
        lines = lines + 1
        await ctx.channel.purge(limit=lines)

    @commands.command()
    async def ticket(self, ctx):
        # async def _create_std_team_room(self, room_name, category):
        category = discord.utils.get(orga.ema_guild.categories, name = "tickets")
        now = datetime.datetime.now()
        now = now.strftime("%H:%M_%d/%m")
        created_room = await registrations_helper._create_std_team_room(self, f"{ctx.message.author.name}_{now}_ticket", category)
        staff_role = discord.utils.get(orga.ema_guild.roles,name="Staff E-magine ⭐")
        await registrations_helper._add_referent_to_team_room(self, ctx.message.author, created_room)
        await created_room.send(f"[ewb] {ctx.message.author.mention} le {staff_role.mention} est prévenu de l'ouverture de ton ticket, il le prendra en charge dès que possible ...\n**Merci d'en exposer dès maintenant, l'objet avec le plus de détails possible.**")
            
    @commands.command()    
    async def close(self, ctx):
        if ctx.channel.name.endswith("_ticket"):
            await ctx.channel.send(f"[ewb] Ticket clos ! Cette room va disparaitre")
            await ctx.channel.delete()
                    
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