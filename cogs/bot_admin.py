
from discord.ext import commands

import discord

import helpers.templates_to_publish as templates
import config_files.ewb_bot as ewb_config

import config_files.organization as orga
# import helpers._discord_server_helper as server_helper
# import helpers.registrations_helper as registrations_helper

import datetime, time



from discord.ext import tasks

class BotAdmin(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        self.clear_spam_log.start()
        self.clear_raid_detect.start()

    @commands.command(name="clear", aliases = ["erase"])
    @commands.has_permissions(manage_messages = True)
    async def clear(self, ctx, lines:int):
        """Nettoie la room"""
        lines = lines + 1
        await ctx.channel.purge(limit=lines)
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def checkRoomID(self, ctx):
        if "ecup" in ctx.message.content:
            tournament = self.ewb.ecup
        tournament.teams_list = tournament.get_registrations_teams_list()
        o = 0
        full = 0
        mixt = 0
        for x in tournament.teams_list:
            if x['ewb_RoomID']:
                if x['ewb_Roster'] == "Mixt":
                    mixt = mixt + 1
                if x['ewb_Roster'] == "Full":
                    full = full + 1
                o = o + 1
                channel = self.ewb.get_channel(x['ewb_RoomID'])
                # if str(x['ewb_RoomID']) == str(channel.id):
                    # await ctx.send(f"{o}. {channel.mention} id:{channel.id} onSheet:{x['ewb_RoomID']}")
                #     pass
                # else:
                #     pass
                    # await ctx.send(f"> NOK {channel.mention} id:{channel.id} onSheet:{x['ewb_RoomID']}")
        await ctx.send(f"mixt : {mixt} | full : {full}")
    
    @commands.command()
    async def ticket(self, ctx):
        # async def _create_std_team_room(self, room_name, category):
        category = discord.utils.get(orga.ema_guild.categories, name = "tickets")
        now = datetime.datetime.now()
        now = now.strftime("%H:%M_%d/%m")
        created_room = await registrations_helper._create_std_team_room(self, f"{ctx.message.author.name}_{now}_ticket", category)
        staff_role = discord.utils.get(orga.ema_guild.roles,name="Staff E-magine ⭐")
        await registrations_helper._add_referent_to_team_room(self, ctx.message.author, created_room)
        await created_room.send(f"[ewb] {ctx.message.author.mention} le {staff_role.mention} est prévenu de l'ouverture de ton ticket, il le prendra en charge dès que possible ...\n**Merci d'en exposer dès maintenant, l'objet avec le plus de détails possible.**")
    
    @commands.command()
    async def renameRooms(self, ctx):
        for channel in self.ewb.get_all_channels():
            if str(channel.category) == "Mixt" or str(channel.category) == "Full":
                if "⚠" in str(channel.name):
                    new_name = channel.name.replace("⚠","")
                    await channel.edit(name = new_name)
                    
                    
    @commands.command()    
    async def close(self, ctx):
        if ctx.channel.name.endswith("_ticket"):
            await ctx.channel.send(f"[ewb] Ticket clos ! Cette room va disparaitre")
            await ctx.channel.delete()
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def check(self, ctx, message=None):
        # _global_check_tournament
        if "ecup" in ctx.message.content:
            tournament = self.ewb.ecup
        tournament.teams_list = tournament.get_registrations_teams_list()
        o = await registrations_helper._check_if_double_tag_use(self, tournament.teams_list)
        errors = []
        errors_names = []
        errors_blasons = []
        errors_valid = []
        no_room = []
        for x in tournament.teams_list:
            if x['ewb_Tag'] in o:
                try:
                    channel = self.ewb.get_channel(x['ewb_RoomID'])
                    errors.append(f"> **`{x['ewb_Tag']}`** {channel.mention}")
                    await channel.send(f"[ewb] Attention votre tag `{x['ewb_Tag']}`` est aussi utilisé par une autre équipe")
                except: 
                    errors.append(f"> **`{x['ewb_Tag']}`** {x['ewb_NomEquipe']} {x['ewb_Roster']}")
        o = await registrations_helper._check_if_double_name_use(self, tournament.teams_list)
        
        for x in tournament.teams_list:
            if x['ewb_NomEquipe'] in o:
                try:
                    channel = self.ewb.get_channel(x['ewb_RoomID'])
                    errors_names.append(f"> **`{x['ewb_NomEquipe']}`** {channel.mention}")
                    # await channel.send(f"[ewb] Attention votre nom d'équipe `{x['ewb_NomEquipe']}`` est aussi utilisé par une autre équipe")
                except: 
                    errors_names.append(f"**`{x['ewb_NomEquipe']}`** {x['ewb_Tag']} {x['ewb_Roster']}")            
        o = await registrations_helper.check_if_no_blason(self, tournament.teams_list)
        
        for x in tournament.teams_list:
            if x['ewb_NomEquipe'] in o:
                try:
                    channel = self.ewb.get_channel(x['ewb_RoomID'])
                    errors_blasons.append(f"> **`{x['ewb_NomEquipe']}`** {channel.mention}")
                    if message:
                        await channel.send(f"[ewb] Sauf erreur, nous n'avons pas de blason, pour votre équipe, merci de nous le transmettre au plus vite !")
                except:
                    errors_blasons.append(f"> **`{x['ewb_NomEquipe']}`**")
                    no_room.append(f"> **`{x['ewb_NomEquipe']}`**")

        for x in tournament.teams_list:
            print(x['ewb_infosOK'])
            if x['ewb_infosOK'] != "TRUE":
                if x['ewb_RoomID'] != "":
                    channel = self.ewb.get_channel(x['ewb_RoomID'])
                errors_valid.append(f"> **`{x['ewb_NomEquipe']}`** {channel.mention}")
                if x['ewb_RoomID'] != "" and message:
                    await channel.send(f"[ewb] Sauf erreur, vous n'avez pas validée les informations de votre inscriptions. **Merci de donner signe de vie rapidement !**")

        if len(errors_names) > 0:
            await ctx.send(f"[ewb] Nom(s) d'équipe utilisés par deux équipes : {len(errors_names)}")
            await ctx.send('\n'.join(errors_names))
        if len(errors) > 0:
            await ctx.send(f"[ewb] Tag(s) utilisés par deux équipes : {len(errors)}")
            await ctx.send('\n'.join(errors))
        if len(errors_blasons) > 0:
            await ctx.send(f"[ewb] Équipe(s) sans blason : {len(errors_blasons)}")
            await ctx.send('\n'.join(errors_blasons))
        if len(errors_valid) > 0:
            await ctx.send(f"[ewb] Équipe(s) n'ayant pas confirmé les infos : {len(errors_valid)}")
            await ctx.send('\n'.join(errors_valid))
        if len(no_room) > 0:
            await ctx.send(f"[ewb] Équipe(s) n'ayant pas de room : {len(no_room)}")
            await ctx.send('\n'.join(no_room))

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def copieRoom(self, ctx, name=None):
        if not name:
            name = f"DUPLICATE {ctx.channel.name}"
        new = await ctx.channel.clone(name=name, reason="Has been nuked")
        await new.send(f"{ctx.message.author.mention} room créée à partir de {ctx.channel.mention}")
        await new.send(new.changed_roles)
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def mentionables(self, ctx, select, action):
        """ Gère le paramètre "Mentionable" des rôles équipes """
        await ctx.send(await server_helper._mentionable_roles(self, select, action))
                    
    @tasks.loop(seconds=ewb_config.timing_spam_detect)
    async def clear_spam_log(self):
        with open("data/temp/spam.txt", "r+") as file:
            file.truncate(0)
            # print("[ewb.BotAdmin] spam log cleared")
    
    @tasks.loop(seconds=ewb_config.timing_raid_detect)
    async def clear_raid_detect(self):
        with open("data/temp/entry.txt", "r+") as file:
            file.truncate(0)
            # print("[ewb.BotAdmin] entry log cleared")

def setup(bot):
    bot.add_cog(BotAdmin(bot))