
import discord
from discord.ext import commands

# import helpers.templates_to_publish as templates/
import config_files.ewb_bot as ewb_config

import config_files.organization as orga

import datetime, time

class TicketSystem(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command(aliases = ['newTicket'])
    async def ticket(self, ctx):
        """Ouvre un ticket, et en préviens le Staff E-magine
        - ema.ticket
        """
        category = discord.utils.get(orga.ema_guild.categories, name = "tickets")
        now = datetime.datetime.now()
        now = now.strftime("%H:%M_%d/%m")
        created_room = await registrations_helper._create_std_team_room(self, f"{ctx.message.author.name}_{now}_ticket", category)
        staff_role = discord.utils.get(orga.ema_guild.roles,name="Staff E-magine ⭐")
        await registrations_helper._add_referent_to_team_room(self, ctx.message.author, created_room)
        await created_room.send(f"[ewb] {ctx.message.author.mention} le {staff_role.mention} est prévenu de l'ouverture de ton ticket, il le prendra en charge dès que possible ...\n**Merci d'en exposer dès maintenant, l'objet avec le plus de détails possible.**")
            
    @commands.command(aliases = ['close'])    
    async def closeTicket(self, ctx):
        """Ferme le ticket en cours
        - ema.closeTicket
        """
        if ctx.channel.name.endswith("_ticket"):
            await ctx.channel.send(f"[ewb] Ticket clos ! Cette room va disparaitre")
            await ctx.channel.delete()

def setup(bot):
    bot.add_cog(TicketSystem(bot))