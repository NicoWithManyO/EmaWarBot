
import discord
from discord.ext import commands

import helpers.templates_to_publish as templates
import config_files.ewb_bot as ewb_config

import config_files.organization as orga

import datetime, time
import os
import random

from discord.ext import tasks

class BotAdmin(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        self.clear_spam_log.start()
        self.clear_raid_detect.start()
        
    @commands.command(name="reset_roles")
    @commands.has_role("Staff E-magine ⭐")
    async def reset_roles(self, ctx):
        # guild = ctx.get_guild(after.guild.id)
        ecl_role = discord.utils.get(ctx.guild.roles, name="🔴+Référent Ecl")
        ecup_role = discord.utils.get(ctx.guild.roles, name="🔵+Référent Ecup")
        rkg_role = discord.utils.get(ctx.guild.roles, name="🔶+Référent Ranking")
        ref_role = discord.utils.get(ctx.guild.roles, name="☄️-Référent")
        for _ in ctx.guild.members:
            if rkg_role in _.roles or ecl_role in _.roles or ecup_role in _.roles:
                if ref_role not in _.roles:
                    await _.add_roles(ref_role)
                    await ctx.send(f"{_} {ref_role}")
                else:
                    await ctx.send(f"{_} à déjà {ref_role} !")
                await _.remove_roles(rkg_role)
                await _.remove_roles(ecl_role)
                await _.remove_roles(ecup_role)
                
                
    @commands.command(name="clear", aliases = ["erase"])
    @commands.has_role("Staff E-magine ⭐")
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
    @commands.has_role("Staff E-magine ⭐")
    async def clear_raid_detect(self):
        with open("data/temp/entry.txt", "r+") as file:
            file.truncate(0)
            # print("[ewb.BotAdmin] entry log cleared")


    @commands.command(name="invite", aliases = ["invit", "lien"])
    async def invit(self, ctx):
        """ Renvoi le lien d'invitation du serveur. A partager ... """
        await ctx.send(embed = templates.create_std_embed(self, ctx, title = "Partagez ce lien pour inviter vos amis sur E-magine Gaming", desc = f"> ** https://discord.gg/4yAZ2wV **\n\nLiens utiles : [Calendrier](https://s.divlo.fr/CalendrierEma) | [Twitter Ema](https://twitter.com/emagine_gaming?lang=fr)"))
        print(f"Retrouvez aussi : le [Calendrier](https://s.divlo.fr/CalendrierEma) | [Twitter Ema](https://twitter.com/emagine_gaming?lang=fr)")

    
    @commands.command(aliases = ['rtfm'])
    async def rtfr(self, ctx):
        """ ^^ """
        await ctx.send("https://cdn.discordapp.com/attachments/860198153047113789/899596293750521866/RTFR.png")

    @commands.command()
    async def meme(self, ctx):
        pics_list = os.listdir("data/pics/")
        current = random.sample(pics_list, 1)
        current =  "data/pics/"+current[0]
        print(current)
        with open(current, 'rb') as f:
            picture = discord.File(f)
            await ctx.send(file=picture)

def setup(bot):
    bot.add_cog(BotAdmin(bot))
