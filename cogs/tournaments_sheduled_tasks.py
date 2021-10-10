
import discord
from discord.ext import commands
from discord.ext import tasks

import modules.tournaments_manager as tournaments_manager
import config_files.tournaments_config as tournaments_config

import helpers.templates_to_publish as templates

import config_files.ewb_bot as ewb_config

class TournamentsSheduledTasks(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        self.registrations_watcher.start()
        
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

    @tasks.loop(seconds=30)
    async def registrations_watcher(self):
        tournament = None
        channel = self.ewb.get_channel(ewb_config.registrations_log_channel)
        for x in tournaments_config.active_tournaments:
            if x == "ecup":
                tournament = self.ewb.ecup
            if x == "ranking":
                tournament = self.ewb.ranking
            new_registrations_list = tournament.get_new_registrations_list()
            # print(tournament.config_file.registrations_is_open)
            if tournament.config_file.registrations_is_open:
                if new_registrations_list:
                    to_show = templates.create_registrations_embed(self, tournament, new_registrations_list)
                    for x in to_show:
                        await channel.send(embed = x)
                else:
                    print(f"{tournament} no new registration")
            
            
            
            
            
            # print(tournament)
            # old = tournament.current_registrations_number
            # print(old)
            # print(tournament.check_number_of_registrations())

            


            # tournament.get_registrations_teams_list()
            # print(tournament.current_registrations_number)
            # tournament.announce_new_registration()
            
            
        


    

def setup(bot):
    bot.add_cog(TournamentsSheduledTasks(bot))
