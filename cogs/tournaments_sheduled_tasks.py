
import discord
from discord.ext import commands
from discord.ext import tasks

import modules.tournaments_manager as tournaments_manager
import config_files.tournaments_config as tournaments_config

import helpers.templates_to_publish as templates

import config_files.ewb_bot as ewb_config

import helpers.teams_helper as teams_helper
import helpers.gsheet_helper as gsheet_helper

class TournamentsSheduledTasks(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        # self.start_registrations_detection()
        # self.registrations_watcher.start()
        
        # tournaments init
        for x in tournaments_config.active_tournaments:
            if x == "ecup":
                self.ewb.ecup = tournaments_manager.Ecup()
                print(self.ewb.ecup)
            if x == "ranking":
                self.ewb.ranking = tournaments_manager.Ranking()
                print(self.ewb.ranking)
            if x == "ecl":
                self.ewb.ecl = tournaments_manager.Ecl()
                print(self.ewb.ecl)
    
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def temp(self, ctx, *value):
        print(value)
        ref = await teams_helper.search_referent(self, ' '.join(value))
        print(ref)
        for x in ref:
            print(discord.__version__)
            await ctx.send(x.name)
            await ctx.send(x.display_name)
            await ctx.send(x.display_avatar)
            await ctx.send(x.discriminator)
            await ctx.send(x.mention)
# Attributes
# avatar
# bot
# discriminator
# display_name
# mention
# name
    
    
    def start_registrations_detection(self):
        self.registrations_watcher.start()
        return f"[ewb] RegistrationsWatcher `on`"
    def stop_registrations_detection(self):
        self.registrations_watcher.stop()
        return f"[ewb] RegistrationsWatcher `off`"
    
    # def check_teams_referent(self, teams_list):
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def regWatcher(self, ctx, value):
        if value == "on".lower():
            await ctx.send(self.start_registrations_detection())
        elif value == "off".lower():
            await ctx.send(self.stop_registrations_detection())
            
    
    @tasks.loop(seconds=60)
    async def registrations_watcher(self):
        tournament = None
        channel = self.ewb.get_channel(ewb_config.registrations_log_channel)
        for x in tournaments_config.active_tournaments:
            if x == "ecup":
                tournament = self.ewb.ecup
            if x == "ranking":
                tournament = self.ewb.ranking
            new_registrations_list = tournament.get_new_registrations_list()
            if tournament.config_file.registrations_is_open:
                if new_registrations_list:
                    for team in new_registrations_list:
                        ref = await teams_helper.search_referent(self, team['ewb_Ref1'])
                        if len(ref) == 1:
                            for user in ref:
                                await channel.send(f"{user.mention}")
                        else:
                            await channel.send(f"Trop de correspondance pour Ref1")
                        if team['ewb_Ref2'] != "":
                            ref = await teams_helper.search_referent(self, team['ewb_Ref2'])
                            if len(ref) == 1:
                                for user in ref:
                                    await channel.send(f"{user.mention}")
                            else:
                                await channel.send(f"Trop de correspondance pour Ref2")
                    to_show = templates.create_registrations_embed(self, tournament, new_registrations_list)
                    for x in to_show:
                        await channel.send(embed = x)
                        await channel.send("Cet affichage vous confirme que votre inscription est reçue. **Comprenez bien qu'elle doit être confirmée et validée**, dans les plus bref délais ! Sans quoi elle ne sera pas prise en compte\n-")
                else:
                    print(f"{tournament} registrations : {len(tournament.registrations_teams_list)} no new registration")
            print(tournament)
            # print(tournament.registrations_teams_list)

def setup(bot):
    bot.add_cog(TournamentsSheduledTasks(bot))
