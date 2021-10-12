
import discord
from discord.ext import commands

import helpers.tournaments_helper as tournaments_helper

import helpers.templates_to_publish as templates

class TournamentsManager(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def voir(self, ctx, *id_team):
        id_team = ' '.join(id_team)
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        for team in teams_to_show:
            print(team['ewb_NomEquipe'])
            # print(team['ewb_NomEquipe'])
        # to_show = []
        # if id_team == None:
        #     for team in data:
        #         if team['ewb_Ref1'] in str(ctx.message.author) or str(ctx.message.author) in team['ewb_Ref1']:
        #             to_show.append(team)
        #     embed = templates.create_registrations_embed(self, tournament, to_show)
        #     for x in embed:
        #         await ctx.send(embed = x)
        # else:
        #     try:
        #         id_team = int(id_team)
        #         # search by ID (int)
        #         for team in data:
        #             if team['ewb_ID'] == id_team:
        #                 to_show.append(team)
        #     except:
        #         print("nok INT")
        # if len(to_show) > 0:
        #     print(to_show)
        #     for x in to_show:
        #         print(x['ewb_ID'])

def setup(bot):
    bot.add_cog(TournamentsManager(bot))