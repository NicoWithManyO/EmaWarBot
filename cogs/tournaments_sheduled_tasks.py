
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

    def start_registrations_detection(self):
        self.registrations_watcher.start()
        return f"[ewb] RegistrationsWatcher `on`"
    def stop_registrations_detection(self):
        self.registrations_watcher.stop()
        return f"[ewb] RegistrationsWatcher `off`"

    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def regWatcher(self, ctx, value):
        if value == "on".lower():
            await ctx.send(self.start_registrations_detection())
        elif value == "off".lower():
            await ctx.send(self.stop_registrations_detection())

    @tasks.loop(seconds=120)
    async def registrations_watcher(self):
        tournament = None
        channel = self.ewb.get_channel(ewb_config.registrations_log_channel)
        for x in tournaments_config.active_tournaments:
            # if x == "ecup":
            #     tournament = self.ewb.ecup
            if x == "ranking":
                tournament = self.ewb.ranking
            new_registrations_list = tournament.get_new_registrations_list()
            if tournament.config_file.registrations_is_open:
                if new_registrations_list:
                    for team in new_registrations_list:
                        print(tournament)
                        await channel.send(f"> [ewb] Réception de {team['ewb_NomEquipe']}")
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
                    to_show = await templates.create_registrations_embed(self, tournament, new_registrations_list)
                    for x in to_show:
                        await channel.send(embed = x)
                        print(team['ewb_New'])
                        print(type(team['ewb_New']))
                        
                        if team['ewb_New'] == "FALSE":
                            await channel.send(f"> [ewb] L'équipe **`{team['ewb_NomEquipe']}`** à déjà participé, après avoir vérifier les données (particulièrement le Roster **`{team['ewb_Roster']}`** et votre tag clan **`{team['ewb_Tag']}`**) vous pouvez ajouter :white_check_mark:, nous validerons dès que possible ...")
                        else:
                            await channel.send(f"> [ewb] Bienvenue dans le Ranking, merci de vérifier les informations de votre inscription (le roster d'inscription particulièrement **`{team['ewb_Roster']}`**, ainsi que le nom de votre équipe **`{team['ewb_NomEquipe']}`**, sans oublier le tag du **clan dans le quel vous jouerez le match `{team['ewb_Tag']}`**) ... **Merci ensuite de prendre contact (dans le #flood ou les rooms #ewb_check) avec le @Staff E-magine**, afin que nous validions définitivement votre inscription !")
                else:
                    print(f"{tournament} registrations : {len(tournament.registrations_teams_list)} no new registration")
            print(tournament)

def setup(bot):
    bot.add_cog(TournamentsSheduledTasks(bot))
