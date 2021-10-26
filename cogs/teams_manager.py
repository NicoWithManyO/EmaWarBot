
import discord
from discord.ext import commands

import datetime
import time

import helpers.tournaments_helper as tournaments_helper

import helpers.templates_to_publish as templates

import helpers.gsheet_helper as gsheet
import helpers.ingame_helper as ingame
import validators

import helpers.teams_helper as teams_helper

import config_files.emojis as emojis

import random

class TeamsManager(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb       

    
    @commands.command(aliases = ["mbr", "user", "member"])
    async def membre(self, ctx, *utilisateur):
        """Retourne les utilisateur contenant la chaine recherchée
        
        Fournir un morceau de nom ou un discriminator (ex. #8020) à rechercher
        - ema.membre nicowithmany
        - ema.membre 8020
        (La recherche n'est pas sensible à la casse)
        """        
        o = 0
        querry = ' '.join(utilisateur)
        if len(querry) < 4:
            await ctx.send("[ewb] 4 caracètres mini. pour la recherche")
            return
        matched = await teams_helper.search_discord_user(self, querry)
        if len(matched) == 0:
            await ctx.send("[ewb] Pas de résultat !")
            return
        if len(matched) == 1:
            await ctx.send("[ewb] Quick User Checker\n[ewb] Utilisateur trouvé :")
            await ctx.send(f"> {emojis.discord} {matched[0].mention} `{matched[0]}` {matched[0].id}")
        else:
            await ctx.send(f"[ewb] Quick User Checker\n[ewb] {len(matched)} résultats")
            for finded in matched:
                o = o + 1
                await ctx.send(f"> {emojis.discord} `{o}.` {finded.mention} `{finded}` {finded.id}")
    
    
    @commands.command()
    async def voir(self, ctx, *id_team):
        if ctx.message.content.startswith("ema.") or ctx.message.content.startswith("Ema."):
            await ctx.send(f"> [ewb] Utiliser le prefix pour selectioner une compétition `rkg.voir` ou `ecup.voir`")
        id_team = ' '.join(id_team)
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        if id_team == "info" or id_team == "infos" or id_team == "compet":
            desc = f"{tournament.config_file.description}\n\n{tournament.config_file.liens_utiles}\n{tournament.config_file.translate_links}"
            await ctx.send(embed = templates.create_std_embed(self, ctx, color = tournament.config_file.color, title = f"{tournament}", desc = f"{desc}", logo = tournament.tournament_avatar))
            return
        
        ## doit passer tests
        # if tournament.name == "Ecup":
        #     print(ctx.message.channel.id)
        #     for temp in data:
        #         if temp['ewb_RoomID'] == ctx.message.channel.id:
        #             id_team = int(temp['ewb_ID'])
        # print(to_show)

        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if teams_to_show:
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            
            for x in embeds:
                await ctx.send(embed = x)
        else:
            await ctx.send("> [ewb] Pas de résultat. Essayer `rkg.voir NomEquipe` ou `ecup.voir NomEquipe`")

    
    @commands.command()
    async def recap(self, ctx, option=None):
        mixt_validated = []
        full_validated = []
        mixt_to_check = []
        full_to_check = []
        mixt_canceled = []
        full_canceled = []
        mixt_all = []
        full_all = []
    
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()

        for team in data:
            if team['ewb_Roster'] == "Mixt":
                mixt_all.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
                if team['ewb_FinalState'] == "Validée":
                    mixt_validated.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
                if team['ewb_FinalState'] == "Annulée" or team['ewb_FinalState'] == "Refusée" :
                    mixt_canceled.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
                if team['ewb_FinalState'] == "En attente de validation":
                    mixt_to_check.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
            if team['ewb_Roster'] == "Full":
                full_all.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
                if team['ewb_FinalState'] == "Validée":
                    full_validated.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
                if team['ewb_FinalState'] == "Annulée" or team['ewb_FinalState'] == "Refusée" :
                    full_canceled.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
                if team['ewb_FinalState'] == "En attente de validation":
                    full_to_check.append(f"`{team['ewb_ID']}` {team['ewb_NomEquipe']}")
        
        await ctx.send(f"> [ewb] `{tournament}`\n> **{len(mixt_all)}** {emojis.mixt}ixt")
        await ctx.send(f"**__{len(mixt_to_check)} reste(s) à valider :__ {' | '.join(mixt_to_check)}**")
        await ctx.send(f"__{len(mixt_validated)} validée(s) :__ {' | '.join(mixt_validated)}")
        await ctx.send(f"__{len(mixt_canceled)} annulée(s) / refusée(s) :__ {' | '.join(mixt_canceled)}")
        await ctx.send(f"> **{len(full_all)}** {emojis.full}ull")
        await ctx.send(f"**__{len(full_to_check)} reste(s) à valider :__ {' | '.join(full_to_check)}**")
        await ctx.send(f"__{len(full_validated)} validée(s) :__ {' | '.join(full_validated)}")
        await ctx.send(f"__{len(full_canceled)} annulée(s) / refusée(s) :__  {' | '.join(full_canceled)}")
        if len(mixt_to_check) == 0 and len(full_to_check) == 0:
            await ctx.send(f"Good Job le Staff !")
        if option == "tos":
            response = await ctx.send(f"> [ewb] Utiliser {emojis.mixt} ou {emojis.full} pour lancer un tirage au sort")
            if tournament.name == "Ecup":
                self.ewb.ecup.config_file.registration_recap_msg = response.id
            if tournament.name == "Ranking":
                self.ewb.ranking.config_file.registration_recap_msg = response.id
            
                
            # print(type(tournament.config_file.registration_recap_msg))
        
    @commands.command()
    async def liste(self, ctx, roster=None):
        mixt = []
        full = []
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        for team in data:
            current = f"`{team['ewb_ID']}`. {team['ewb_NomEquipe']}"
            if team['Validée'] != "TRUE" and team['Refusée'] == "FALSE":
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
            
    @commands.command(aliases = ["v"])
    @commands.has_role("Staff E-magine ⭐")
    async def valid(self, ctx, id_team:int): 
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if teams_to_show:
            for team in teams_to_show:
                row = team['ewb_ID'] + 1
                old = team['ewb_Valid']
                target = f"EA{row}"
                new_value = True
                await ctx.send(f"> [ewb] `{tournament}` **validation OK** pour **{team['ewb_NomEquipe']}** {team['ewb_Roster']} (ancien : <{old}>)")
                gsheet.set_data_team_to_sheet(tournament, target, new_value)
                target = f"ED{row}"
                gsheet.set_data_team_to_sheet(tournament, target, str(ctx.message.author.display_name))
                
    
    @commands.command()
    # @commands.has_permissions(manage_messages = True)
    @commands.has_role("Staff E-magine ⭐")
    async def change(self, ctx, id_team:int, object_to_change, new_value=None):
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        # if tournament.name == "Ecup":
        #     print(ctx.message.channel.id)
        #     for temp in data:
        #         if temp['ewb_RoomID'] == ctx.message.channel.id:
        #             id_team == int(temp['ewb_RoomID'])
        print(new_value)
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if new_value.startswith("<@!") or new_value.startswith("<@"):
            if new_value.startswith("<@!"):
                new_value = new_value.replace("<@!","").replace(">","")
            if new_value.startswith("<@"):
                new_value = new_value.replace("<@","").replace(">","")
            new_value = int(new_value)
            new_member = discord.utils.get(ctx.guild.members,id=int(new_value))
            new_value = new_member
        else:        
            new_value = str(''.join(new_value))
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
                        new_value = True
                    if new_value == "-":
                        new_value = False
                if object_to_change.lower() == "cancel":
                    target = f"EB{row}"
                    old = team['ewb_Valid']
                    if new_value == "+":
                        new_value = True
                    if new_value == "-":
                        new_value = False

            await ctx.send(f"> [ewb] `{tournament}` Modification de **{object_to_change}** pour **{team['ewb_NomEquipe']}** {team['ewb_Roster']} (ancien : <{old}>)")
            
            if object_to_change == "valid":
               gsheet.set_data_team_to_sheet(tournament, target, new_value)
               target = f"ED{row}"
               gsheet.set_data_team_to_sheet(tournament, target, str(ctx.message.author.display_name))
            else:    
                gsheet.set_data_team_to_sheet(tournament, target, str(new_value))

            data = tournament.get_registrations_teams_list()
            teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author.name)
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            for x in embeds:
                first_response = await ctx.send(embed = x)
        else:
            pass
 
def setup(bot):
    bot.add_cog(TeamsManager(bot))
