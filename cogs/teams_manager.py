
import discord
from discord.ext import commands

import helpers.tournaments_helper as tournaments_helper

import helpers.templates_to_publish as templates

import helpers.gsheet_helper as gsheet
import helpers.ingame_helper as ingame
import validators

import config_files.emojis as emojis

class TeamsManager(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command()
    @commands.has_permissions(manage_messages = True)
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
                row = team['ewb_ID'] + 1
                print(team)
                if object_to_change == "blason":
                    if validators.url(new_value):
                        old = team['ewb_urlBlason']
                        target = f"AW{row}"
                    else:
                        await ctx.send(f"[ewb] `{new_value}` ne semble pas être une URL")
                        return
                if object_to_change == "tag":    
                    try:
                        old = team['ewb_Tag']
                        clan = await ingame.check_clan_tag(self, new_value)
                        target = f"AV{row}"
                        await ctx.send(f"> [ewb] {emojis.clan_ok} `{clan.tag}` {clan.name} {clan.public_war_log}")
                    except:
                        await ctx.send(f"> [ewb] {emojis.clan_nok} `{new_value}` ne semble pas être un tag valide")
                        return

            await ctx.send(f"> [ewb] `{tournament}` Modification de **{object_to_change}** pour **{team['ewb_NomEquipe']}** (ancien : <{old}>)")
            gsheet.set_data_team_to_sheet(tournament, target, new_value)
            data = tournament.get_registrations_teams_list()
            teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            for x in embeds:
                await ctx.send(embed = x)
        else:
            await ctx.send("o")
            
def setup(bot):
    bot.add_cog(TeamsManager(bot))