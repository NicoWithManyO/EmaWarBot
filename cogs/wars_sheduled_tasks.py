
import coc

import discord
from discord.ext import commands
from discord.ext import tasks

import modules.tournaments_manager as tournaments_manager
import config_files.tournaments_config as tournaments_config

import helpers.ingame_helper as ingame
import helpers.gsheet_helper as gsheet
import config_files.ewb_bot as ewb_config
import config_files.emojis as emojis

class WarsSheduledTasks(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb
        # self.start_round_matchs_detection()
        

    def stop_round_matchs_detection(self):
        self.scores_watcher.stop()
        return f"[ewb.WarsWatcher] `off`"
    def start_round_matchs_detection(self):
        self.scores_watcher.start()
        return f"[ewb.WarsWatcher] `on`"
    
    @commands.command()
    @commands.has_permissions(manage_messages = True)
    async def getScores(self, ctx, value):
        if value == "on".lower():
            try:
                await ctx.send(self.start_round_matchs_detection())
            except:
                await ctx.send(f"[ewb.WarWatcher] `processus en cours`")
        elif value == "off".lower():
            await ctx.send(self.stop_round_matchs_detection())
    
    # @commands.command()
    # async def addHoraire(self, ctx, )
    
    @commands.command()
    async def horaires(self, ctx):
        tournament = None
        channel = self.ewb.get_channel(ewb_config.war_log_channel)
        for x in tournaments_config.active_tournaments:
            # if x == "ecup":
            #     tournament = self.ewb.ecup
            if x == "ranking":
                tournament = self.ewb.ranking
        self.round_full_matchs_list = tournament.get_horaires_matchs('full')
        self.round_mixt_matchs_list = tournament.get_horaires_matchs('mixt')
        to_check = [self.round_mixt_matchs_list, self.round_full_matchs_list]
        no_declaration = []
        for x in to_check:
            for match in x:
                print(match['ewb_Horaire'])
                ## no testing
                if match['ewb_Horaire'] == "" and match['ewb_Groupe']:
                    no_declaration.append(f"{match['ewb_TeamA']}/{match['ewb_TeamB']}")
        await ctx.send(f"__{len(no_declaration)} sans horaire :__  {' | '.join(no_declaration)}")
        if len(no_declaration) == 0:
            await ctx.send(f"> [ewb] Good Job les Référents !")

    @commands.command()
    async def livewar(self, ctx, tag):
        war = await ingame.check_current_war(self, tag)
        if type(war) == coc.wars.ClanWar:
            # await ctx.send(f"> [ewb.LiveWarWatcher] {war.clan} {emojis.vs} {war.opponent} {war.opponent.tag}")
            await ctx.send(f"[ewb.{emojis.live}] **LIVE SCORE** {war.clan} {war.clan.destruction} **{war.clan.stars}** {emojis.vs} **{war.opponent.stars}** {war.opponent.destruction} {war.opponent} {war.opponent.tag} | {war.state}")
            
            # players = []
            # opp_players = []
            # if len(war.clan.members) < 10:
            #     for player in war.clan.members:
            #         players.append(f"{war.clan.tag}, {player.name}, {player.tag}, TH{player.town_hall}")
            #     for player in war.opponent.members:
            #         opp_players.append(f"{war.opponent.tag}, {player.name}, {player.tag}, TH{player.town_hall}")
            # await ctx.send(f"> [ewb.LiveWarWatcher] {war.clan} {war.clan.tag} {' | '.join(players)}")
            # await ctx.send(f"> [ewb.LiveWarWatcher] {war.opponent} {war.opponent.tag} {' | '.join(opp_players)}")
        else:
            await ctx.send(f"> [ewb.LiveWarWatcher] {war} pour {tag}")
    
    @tasks.loop(seconds=600)
    async def scores_watcher(self):
        print("detection des matchs")
        tournament = None
        channel = self.ewb.get_channel(ewb_config.war_log_channel)
        ended_channel = self.ewb.get_channel(ewb_config.ended_wars_log_channel)
        for x in tournaments_config.active_tournaments:
            # if x == "ecup":
            #     tournament = self.ewb.ecup
            if x == "ranking":
                tournament = self.ewb.ranking
        self.round_full_matchs_list = tournament.get_round_matchs_list('full')
        self.round_mixt_matchs_list = tournament.get_round_matchs_list('mixt')
        to_check = [self.round_mixt_matchs_list, self.round_full_matchs_list]
        await channel.send(f"> [ewb.WarsWatcher] {tournament}")
        o = 0
        launched = 0
        ended = 0
        no_finded = 0
        for x in to_check:
            for match in x:
                if match['ewb_ARecup'] == 'TRUE':
                    o = o + 1
                    roster = match['ewb_IDMatch'][:4]
                    await channel.send(f"> emaMatch `{o}`. `{match['ewb_IDMatch']}` **{roster}** {match['ewb_Tag']} **{match['ewb_TeamA']}** {emojis.vs} **{match['ewb_TeamB']}** {match['ewb_TagOpp']} (prévue : {match['ewb_Horaire']} {match['ewb_ModifDate']})")
                    war = await ingame.check_current_war(self, match['ewb_Tag'])
                    if type(war) == coc.wars.ClanWar:
                        if match['ewb_Tag'] == war.clan.tag:
                            teams_players = []
                            # print(match['ewb_TagOpp'])
                            # print(war.opponent.tag)
                            if match['ewb_TagOpp'] == war.opponent.tag:
                                
                                await channel.send(f"Match détecté : **{roster}** {match['ewb_Tag']} **{match['ewb_TeamA']}** {emojis.vs} **{match['ewb_TeamB']}** {match['ewb_TagOpp']} | {war.state} | {war.team_size}players | startTime{war.start_time}")
                                # await channel.send(f"Adversaire correspondant {match['ewb_Tag']} vs {war.opponent.tag} {war.team_size}players {war.state} | endTime{war.end_time}")
                                if war.state == "inWar":
                                    await channel.send(f"{emojis.live} **LIVE SCORE** {match['ewb_TeamA']} {war.clan.destruction} {war.clan.stars} {emojis.vs} {war.opponent.stars} {war.opponent.destruction} {match['ewb_TeamB']} | {war.state}")
                                    # print(''.join(war.attacks))
                                if war.state == "inWar" or war.state == "warEnded":
                                    launched = launched + 1
                                    if match['ewb_PlayersOK'] == "FALSE":
                                        await channel.send(f"> [ewb] Récupération des joueurs")
                                        players = []
                                        for player in war.clan.members:
                                            players.append([match['ewb_IDMatch'], match['ewb_TeamA'], player.name, player.tag, player.town_hall])
                                        for player in war.opponent.members:
                                            players.append([match['ewb_IDMatch'], match['ewb_TeamB'], player.name, player.tag, player.town_hall])
                                        row = tournament.get_last_row_on_players_data()
                                        target = f"B{row}"
                                        tournament.set_players_teams_list(target, players)
                                    else:
                                        await channel.send(f"Joueurs ok {match['ewb_IDMatch']}")
                                if war.state == "warEnded":
                                    ended = ended + 1
                                    score = [[war.clan.destruction, war.clan.stars, war.opponent.stars, war.opponent.destruction, war.status]]
                                    print(score)
                                    await ended_channel.send(f"> Fin de match : {match['ewb_TeamA']} {war.clan.destruction} **{war.clan.stars}** {emojis.vs} **{war.opponent.stars}** {war.opponent.destruction} {match['ewb_TeamB']} | {war.state}")
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
        await channel.send(f"Total : {o} | Lancé(s) : {launched} | Fini(s) : {ended}")
        # await channel.send(f"> [ewb] fin.")


    
def setup(bot):
    bot.add_cog(WarsSheduledTasks(bot))