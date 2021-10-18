
import discord
from discord.ext import commands

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
        if ctx.message.content.startswith("ema."):
            await ctx.send(f"> [ewb] Utiliser le prefix pour selectioner une compétition `rkg.voir` ou `ecup.voir`")
        id_team = ' '.join(id_team)
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        if id_team == "info" or id_team == "infos" or id_team == "compet":
            # if tournament.name == "Ranking":
            #     desc = f"{tournament.config_file.description}\n\n{tournament.config_file.liens_utiles}\n{tournament.config_file.translate_links}"
            # if tournament.name == "Ecup":
            #     desc = f"Retrouver l'Ecup tous les dimanches soirs !\n(Inscriptions closes)\n{tournament.config_file.liens_utiles}"
            desc = f"{tournament.config_file.description}\n\n{tournament.config_file.liens_utiles}\n{tournament.config_file.translate_links}"
            await ctx.send(embed = templates.create_std_embed(self, ctx, color = tournament.config_file.color, title = f"{tournament}", desc = f"{desc}", logo = tournament.tournament_avatar))
            return
            
        # if tournament.name == "Ecup":
        #     print(ctx.message.channel.id)
        #     for temp in data:
        #         if temp['ewb_RoomID'] == ctx.message.channel.id:
        #             id_team == int(temp['ewb_RoomID'])
        # print(to_show)
        print(data)
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if teams_to_show:
            embeds = await templates.create_registrations_embed(self, tournament, teams_to_show)
            
            for x in embeds:
                print(x)
                await ctx.send(embed = x)
        else:
            await ctx.send("> [ewb] Pas de résultat")
    
    # @commands.command()
    # async def cherche(self, *search):
    #     o = ' '.join(*search)
    #     await gsheet.teams_helper.search_referent(self, search)
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def tos(self, ctx, roster, troll=None):
        final_teams_list = []
        matchs_list = []
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        for team in data:
            if team['ewb_Roster'].lower() == roster.lower():
                if team['ewb_FinalState'] == "Validée":
                    final_teams_list.append(f"{team['ewb_NomEquipe']}")
        await ctx.send(f"{roster} {len(final_teams_list)} équipes : {' `|` '.join(final_teams_list)}")
        nbre_teams = len(final_teams_list)
        # final_teams_list = ["1", "2", "o","zi", "3"]
        pair = []
        pair = []
        matchs_list = []
        exempt = None
        await ctx.send(f"> [ewb] Tirage {tournament} {str(roster).title()}\n{nbre_teams} équipes\n{round(nbre_teams / 2)} matchs")
        while len(final_teams_list) > 0:
            current = random.choice(final_teams_list)
            final_teams_list.remove(current)
            pair.append(current)
            if len(pair) == 2:
                matchs_list.append(pair)
                pair = []
        print(len(final_teams_list))
        print(pair)
        if pair:
            await ctx.send(f"exempt : {pair[0]}")
            exempt = pair[0]
        # await ctx.send(matchs_list)
        o = 0
        for match in matchs_list:
            o = o + 1
            if troll != "notroll":
                await ctx.send(f"`{o}`.||**{match[0]}**|| `vs` ||**{match[1]}**||")
                if exempt:
                    await ctx.send(f"Exempt : {exempt}")
            else:
                await ctx.send(f"`{o}`.**{match[0]}** `vs` **{match[1]}**")
                if exempt:
                    await ctx.send(f"Exempt : {exempt}")
        if roster.lower() == "mixt":
            target = f"A1"
            target_exempt = f"C1"
        if roster.lower() == "full":
            target = f"F1"
            target_exempt = f"H1"
        
        print(gsheet.set_data_tos_to_sheet(tournament, target, matchs_list))
        if exempt:
            print(gsheet.set_data_tos_to_sheet(tournament, target_exempt, exempt))
   
    
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
            

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def change(self, ctx, id_team:int, object_to_change, *new_value):
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        # if tournament.name == "Ecup":
        #     print(ctx.message.channel.id)
        #     for temp in data:
        #         if temp['ewb_RoomID'] == ctx.message.channel.id:
        #             id_team == int(temp['ewb_RoomID'])
        teams_to_show = tournaments_helper.teams_selector(self, id_team, data, ctx.message.author)
        if new_value[0].startswith("<@!"):
            new_value = new_value[0].replace("<@!","").replace(">","")
            new_value = int(new_value)
            new_member = discord.utils.get(ctx.guild.members,id=int(new_value))
            new_value = new_member
            # await ctx.send(f"[ewb.debug] {new_value} / {new_member.name} / {new_value.display_name} {new_value.avatar_url}")
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
                    await ctx.send(f"[ewb.debug] {new_value} / {new_value} / url_avatar <new_value.avatar_url> / {new_value.id}")
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