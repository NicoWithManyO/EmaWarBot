
import discord
from discord.ext import commands

import helpers.templates_to_publish as templates
import config_files.ewb_bot as ewb_config

import helpers.tournaments_helper as tournaments_helper

from discord.ext import tasks

class PLayersManager(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command()
    async def joueur(self, ctx, player_tag):
        """ Recherche si un (tag) joueur à joué dans la compétition """
        if not player_tag.startswith("#"):
            player_tag = f"#{player_tag}"
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        # data = tournament.get_registrations_teams_list()
        response = tournament.get_player_by_tag(player_tag)
        await ctx.send(f"> [ewb] {tournament}\n{''.join(response)}")


def setup(bot):
    bot.add_cog(PLayersManager(bot))
