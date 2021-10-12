
import discord
from discord.ext import commands

import helpers.tournaments_helper as tournaments_helper

import helpers.templates_to_publish as templates

class TeamsManager(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command()
    async def voir(self, ctx, *id_team):
        id_team = ' '.join(id_team)
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if teams_to_show:
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            for x in embeds:
                await ctx.send(embed = x)
        else:
            await ctx.send("> [ewb] Pas de résultat")

    @commands.command()
    async def change(self, ctx, id_team:int, object_to_change, *new_value):
        
        new_value = str(' '.join(new_value)).lower()
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if teams_to_show:
            for team in teams_to_show:
                print(team)
                if object_to_change == "blason":
                    await ctx.send(f"> [ewb] `{tournament}` Modification de **{object_to_change}** pour **{team['ewb_NomEquipe']}** (ancien : <{team['ewb_urlBlason']}>)")
                
            data = tournament.get_registrations_teams_list()
            teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            for x in embeds:
                await ctx.send(embed = x)        
        else:
            await ctx.send("o")
            
def setup(bot):
    bot.add_cog(TeamsManager(bot))