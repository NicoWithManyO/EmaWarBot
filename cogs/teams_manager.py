
import discord
from discord.ext import commands

import helpers.tournaments_helper as tournaments_helper

import helpers.templates_to_publish as templates

import helpers.gsheet_helper as gsheet
import helpers.ingame_helper as ingame
import validators

import helpers.teams_helper as teams_helper

import config_files.emojis as emojis

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
    async def liste(self, ctx, roster=None):
        mixt = []
        full = []
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        for team in data:
            current = f"`{team['ewb_ID']}`. {team['ewb_NomEquipe']}"
            if team['Validée'] != "TRUE":
                if team['ewb_Roster'] == "Mixt":
                    mixt.append(current)
                if team['ewb_Roster'] == "Full":
                    full.append(current)
        await ctx.send(f"> [ewb] `{tournament}`")
        if not roster:
            await ctx.send(f"> {len(mixt)} **Mixt** {' '.join(mixt)}")
            await ctx.send(f"> {len(full)} **Full** {' '.join(full)}")
        elif roster.lower() == "m":
            await ctx.send(f"> {len(mixt)} **Mixt** {' '.join(mixt)}")
        else: 
            if roster.lower() == "f":
                await ctx.send(f"> {len(full)} **Full** {' '.join(full)}")
            

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def change(self, ctx, id_team:int, object_to_change, *new_value):
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if new_value[0].startswith("<@!"):
            new_value = new_value[0].replace("<@!","").replace(">","")
            new_value = int(new_value)
            new_member = discord.utils.get(ctx.guild.members,id=int(new_value))
            new_value = new_member.name
        else:        
            new_value = str(' '.join(new_value))
        print(new_value)
        if teams_to_show:
            for team in teams_to_show:
                row = team['ewb_ID'] + 1
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
                if object_to_change.lower() == "ref1":
                    target = f"AS{row}"
                    old = team['ewb_Ref1']
                if object_to_change.lower() == "ref2":
                    target = f"AT{row}"
                    old = team['ewb_Ref2']
                
                if object_to_change.lower() == "valid":
                    target = f"EA{row}"
                    old = team['ewb_Valid']
                    if new_value == "+":
                        new_value = "TRUE"
                    if new_value == "-":
                        new_value = "FALSE"
                if object_to_change.lower() == "cancel":
                    target = f"EB{row}"
                    old = team['ewb_Valid']
                    if new_value == "+":
                        new_value = "TRUE"
                    if new_value == "-":
                        new_value = "FALSE"

            await ctx.send(f"> [ewb] `{tournament}` Modification de **{object_to_change}** pour **{team['ewb_NomEquipe']}** (ancien : <{old}>)")
            gsheet.set_data_team_to_sheet(tournament, target, str(new_value))
            data = tournament.get_registrations_teams_list()
            teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            for x in embeds:
                first_response = await ctx.send(embed = x)
        else:
            pass
            
def setup(bot):
    bot.add_cog(TeamsManager(bot))