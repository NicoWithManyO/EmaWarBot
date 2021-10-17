
import coc

import discord
from discord.ext import commands
from discord.ext import tasks

import modules.tournaments_manager as tournaments_manager
import config_files.tournaments_config as tournaments_config

import helpers.ingame_helper as ingame
import helpers.gsheet_helper as gsheet
import config_files.ewb_bot as ewb_config

class RoundMatchsWatcher(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        self.start_round_matchs_detection()
        

    def stop_round_matchs_detection(self):
        self.scores_watcher.stop()
        return f"[ewb] WarsWatcher `off`"
    def start_round_matchs_detection(self):
        self.scores_watcher.start()
        return f"[ewb] WarsWatcher `on`"
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def getScores(self, ctx, value):
        if value == "on".lower():
            try:
                await ctx.send(self.start_round_matchs_detection())
            except:
                await ctx.send(f"[ewb] WarWatcher `processus en cours`")
        elif value == "off".lower():
            await ctx.send(self.stop_round_matchs_detection())
    
    
    @tasks.loop(seconds=600)
    async def scores_watcher(self):
        print("detection des matchs")
        tournament = None
        channel = self.ewb.get_channel(ewb_config.war_log_channel)
        for x in tournaments_config.active_tournaments:
            if x == "ecup":
                tournament = self.ewb.ecup
            # if x == "ranking":
                # tournament = self.ewb.ranking
        self.round_full_matchs_list = tournament.get_round_matchs_list('full')
        self.round_mixt_matchs_list = tournament.get_round_matchs_list('mixt')
        to_check = [self.round_mixt_matchs_list, self.round_full_matchs_list]
        await channel.send(f"> [ewb] WarWatcher")
        # print(to_check)
        for x in to_check:
            for match in x:
                if match['ewb_ARecup'] == 'TRUE':
                    await channel.send(f"> emaMatch `{match['ewb_IDMatch']}` **{match['ewb_TeamA']}** {match['ewb_Tag']} VS {match['ewb_TagOpp']} **{match['ewb_TeamB']}**")
                    war = await ingame.check_current_war(self, match['ewb_Tag'])
                    if type(war) == coc.wars.ClanWar:
                        if match['ewb_Tag'] == war.clan.tag:
                            teams_players = []
                            print(match['ewb_TagOpp'])
                            print(war.opponent.tag)
                            if match['ewb_TagOpp'] == war.opponent.tag:
                                
                                await channel.send(f"Adversaire correspondant {match['ewb_Tag']} vs {war.opponent.tag} {war.team_size}players {war.state}")
                                # await channel.send(f"endTime{war.end_time}")
                                if war.state == "inWar":
                                    await channel.send(f"**LIVE SCORE** {war.clan.destruction} {war.clan.stars} VS {war.opponent.stars} {war.opponent.destruction} - {war.state}")
                                if war.state == "inWar" or war.state == "warEnded":
                                    if match['ewb_PlayersOK'] == "FALSE":
                                        await channel.send(f"[ewb] Récupération des joueurs")
                                        players = []
                                        for player in war.clan.members:
                                            players.append([match['ewb_IDMatch'], match['ewb_TeamA'], player.name, player.tag])
                                        for player in war.opponent.members:
                                            players.append([match['ewb_IDMatch'], match['ewb_TeamB'], player.name, player.tag])
                                        row = tournament.get_last_row_on_players_data()
                                        target = f"B{row}"
                                        tournament.set_players_teams_list(target, players)
                                    else:
                                        await channel.send(f"Joueurs ok {match['ewb_IDMatch']}")
                                if war.state == "warEnded":
                                    score = [[war.clan.destruction, war.clan.stars, war.opponent.stars, war.opponent.destruction, war.status]]
                                    print(score)
                                    await channel.send(score)
                                    roster = match['ewb_IDMatch'][:4]
                                    search = str(match['ewb_IDMatch'])
                                    row = tournament.get_match_row_for_score(roster, search)
                                    target = f"BG{row.row}"
                                    tournament.set_score_data(roster, target, score)
                                    
                    else:
                        print("no war type")
                else:
                    # print("Récupération désactivée")
                    pass
        print("fin")
        await channel.send(f"> [ewb] fin.")


    
def setup(bot):
    bot.add_cog(RoundMatchsWatcher(bot))