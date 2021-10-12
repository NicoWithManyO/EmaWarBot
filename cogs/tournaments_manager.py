
import discord
from discord.ext import commands

import helpers.tournaments_helper as tournaments_helper

class TournamentsManager(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def voir(self, ctx, id_team):
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        print(tournament)





def setup(bot):
    bot.add_cog(BotAdmin(bot))