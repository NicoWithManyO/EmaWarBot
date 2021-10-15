
import discord

import random

import validators

import config_files.ewb_bot as ewb_config
import config_files.organization as orga

import helpers.ingame_helper as ingame

import helpers.teams_helper as teams_helper

import config_files.emojis as emojis
import config_files.organization as orga

def random_color():
    return random.randint(0, 16777215)

def create_std_embed(self, ctx, tiny = False, color = None, title = None, desc = None, author = None, logo = None, footer = None):
    if not color:
        color = random_color()
    embed = discord.Embed(title = title, description = desc, color = color)
    if not tiny:
        if not logo:
            embed.set_thumbnail(url=orga.ema_logo)
        else:
            embed.set_thumbnail(url=logo)
        if not footer:
            embed.set_footer(text=f"{footer}", icon_url=ewb_config.bot_avatar)
        else:
            embed.set_footer(text=f"{ewb_config.signature}", icon_url=ewb_config.bot_avatar)
        if not author:
            embed.set_author(name=ctx.guild, icon_url= ctx.guild.icon_url)
        elif not tiny:
            embed.set_author(name=author, icon_url= ctx.guild.icon_url)
    return embed


async def create_registrations_embed(self, tournament, teams_list):
    response = []
    ref_role = discord.utils.get(orga.ema_guild.roles,name=f"{tournament.config_file.referent_role}")
    season_role = discord.utils.get(orga.ema_guild.roles,name=f"{tournament.config_file.season_role}")
    for x in teams_list:
        row = x['ewb_ID'] + 1
        color = tournament.config_file.color
        print(x['ewb_FinalState'])
        if x['ewb_FinalState'] == "Validée":
            title = f"`{x['ewb_ID']}`. {x['ewb_NomEquipe']} {emojis.valid}"
        else:
            title = f"`{x['ewb_ID']}`. {x['ewb_NomEquipe']}"
        if x['ewb_FinalState'] != "":
            state = x['ewb_FinalState']
        else:
            state = "Inscription reçue"
        embed = discord.Embed(title = title, description = f"```{state}```", color = color)
        if validators.url(x['ewb_urlBlason']):
            embed.set_thumbnail(url=x['ewb_urlBlason'])
        else:
            embed.set_thumbnail(url=tournament.tournament_avatar)
        if x['ewb_FinalState'] != "":
            state = x['ewb_FinalState']
        else:
            state = "Inscription reçue"
        try:
            clan = await ingame.check_clan_tag(self, x['ewb_Tag'])
            clan = f"{emojis.clan_ok} **{clan.tag} | [{clan.name}]({clan.share_link})**\nWarlog {clan.public_war_log} | {clan.type} | {clan.required_trophies}tr"
        except:
            clan = f"{emojis.clan_nok} {x['ewb_Tag']} Tag incorrect"
        ref1 = None
        try:
            ref1 = await teams_helper.search_referent(self, x['ewb_Ref1'])            
        except:
            pass
        if not ref1:
            ref1 = f"{emojis.ref_nok} {x['ewb_Ref1']}"
        ref2 = None
        if x['ewb_Ref2'] != "":
            try:
                ref2 = await teams_helper.search_referent(self, x['ewb_Ref2'])
            except:
                ref2 = f"{emojis.ref_nok} {x['ewb_Ref2']}"
        if not ref2:
            ref2 = f"{emojis.ref_nok} {x['ewb_Ref2']}"
        if len(ref1) == 1:
            for user in ref1:
                ref1 = f"{emojis.ref_ok} {user}"
                if x['Validée'] == "TRUE":
                    await user.add_roles(ref_role)
                    await user.add_roles(season_role)
                if x['Validée'] == "FALSE":
                    await user.remove_roles(ref_role)
                    await user.remove_roles(season_role)
        if x['ewb_Ref2'] != "":
            if (ref2):
                if len(ref2) == 1:
                    for user in ref2:
                        ref2 = f"{emojis.ref_ok} {user}"
                        if x['Validée'] == "TRUE":
                            await user.add_roles(ref_role)
                            await user.add_roles(season_role)
                        if x['Validée'] == "FALSE":
                            await user.remove_roles(ref_role)
                            await user.remove_roles(season_role)
        if x['ewb_Roster'] == "Mixt":
            roster = f"{emojis.mixt}ixt"
        if x['ewb_Roster'] == "Full":
            roster = f"{emojis.full}ull"
        embed.set_footer(text=f"Inscription reçue le {x['HORRODATEUR']}", icon_url=ewb_config.bot_avatar)
        embed.set_author(name=tournament, icon_url= tournament.tournament_avatar, url=tournament.config_file.suivi_file)
        embed.add_field(name=f"Roster : {roster}", value=f"{clan}", inline= False)
        print(x['ewb_Ligue'])
        print(tournament.name)
        ligue = "-"
        if tournament.name == "Ecup":
            if x['ewb_Roster'] == "Full":
                if x['ewb_Ligue'] == "W":
                    ligue = "Warden"
                if x['ewb_Ligue'] == "Q":
                    ligue = "Queen"
                if x['ewb_Ligue'] == "K":
                    ligue = "King"
                if x['ewb_Ligue'] == "R":
                    ligue = "Royal"
            groupe = x['ewb_Groupe']
            embed.add_field(name=f"Ligue {ligue}", value=f"Groupe {groupe}", inline= False)
        embed.add_field(name=ref1, value="Référent 1", inline= True)
        if x['ewb_Ref2'] != "":
            embed.add_field(name=ref2, value="Référent 2", inline= True)
        if x['ewb_Language'] != "":
            embed.add_field(name=x['ewb_Language'], value="Langue de prédilection", inline= False)
        response.append(embed)
    return response
    