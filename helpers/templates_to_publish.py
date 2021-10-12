
import discord

import random

import config_files.ewb_bot as ewb_config
import config_files.organization as orga

import config_files.emojis as emojis

def random_color():
    return random.randint(0, 16777215)

def create_std_embed(self, ctx, tiny = False, color = None, title = None, desc = None, author = None, logo = None):
    if not color:
        color = random_color()
    embed = discord.Embed(title = title, description = desc, color = color)
    if not tiny:
        if not logo:
            embed.set_thumbnail(url=orga.ema_logo)
        else:
            embed.set_thumbnail(url=logo)
        embed.set_footer(text=f"{ewb_config.signature}", icon_url=ewb_config.bot_avatar)
        if not author:
            embed.set_author(name=ctx.guild, icon_url= ctx.guild.icon)
        elif not tiny:
            embed.set_author(name=author, icon_url= ctx.guild.icon)
    return embed

def create_registrations_embed(self, tournament, teams_list):
    response = []
    for x in teams_list:
        color = tournament.config_file.color
        title = f"`{x['ewb_ID']}`. {x['ewb_NomEquipe']}"
        if x['ewb_FinalState'] != "":
            state = x['ewb_FinalState']
        else:
            state = "Inscription reçue"
        embed = discord.Embed(title = title, description = f"```{state}```", color = color)
        if x['ewb_urlBlason'] != "":
            embed.set_thumbnail(url=x['ewb_urlBlason'])
        else:
            embed.set_thumbnail(url=tournament.tournament_avatar)
        if x['ewb_FinalState'] != "":
            state = x['ewb_FinalState']
        else:
            state = "Inscription reçue"
        embed.set_footer(text=f"Inscription reçue le {x['HORRODATEUR']}", icon_url=ewb_config.bot_avatar)
        embed.set_author(name=tournament, icon_url= tournament.tournament_avatar, url=tournament.config_file.suivi_file)
        embed.add_field(name=f"Roster : {x['ewb_Roster']}", value=f"**Tag clan : {x['ewb_Tag']}** | Warlog\nClan Name", inline= False)
        embed.add_field(name=x['ewb_Ref1'], value="Référent 1", inline= True)
        if x['ewb_Ref2'] != "":
            embed.add_field(name=x['ewb_Ref2'], value="Référent 2", inline= True)
        if x['ewb_Language'] != "":
            embed.add_field(name=x['ewb_Language'], value="Langue de prédilection", inline= False)
        response.append(embed)
    return response
    