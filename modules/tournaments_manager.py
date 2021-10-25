

import config_files.all_tournaments.ecup as ecup_config
import config_files.all_tournaments.ranking as ranking_config
import config_files.all_tournaments.ecl as ecl_config

import helpers.gsheet_helper as gsheet
import helpers.new_gsheet_helper as new_gsheet

import config_files.emojis as emojis

# def get_registrations_list(self):
#     self.registrations_list = gsheet.get_registrations_list(self)
#     return self.registrations_list


class TournamentsManager():
    def instantiate_tournament(self):
        if isinstance(self, Ranking):
            config_file = ranking_config
        if isinstance(self, Ecl):
            config_file = ecl_config
        if isinstance(self, Ecup):
            config_file = ecup_config
        self.name = config_file.name
        self.code_name = config_file.code_name
        self.emo = config_file.emo
        self.current_season = config_file.current_season
        
        self.config_file = config_file
        self.current_round = gsheet.get_round_on_sheet(self)
        self.tournament_avatar = config_file.tournament_avatar
        self.round_mixt_matchs_list = None
        self.round_full_matchs_list = None
        self.current_registrations_number = 0
        self.validaded_teams_list = None
        self.registrations_teams_list = gsheet.get_registrations(self)
        
        
    def __str__(self):
        return f"{self.emo} {self.name} {emojis.current_season}{self.current_season} | {emojis.current_round}{self.current_round}"

    def get_registrations_teams_list(self):
        self.registrations_teams_list = gsheet.get_registrations(self)
        return self.registrations_teams_list

    def get_round_matchs_list(self, roster):
        self.round_matchs_list = gsheet.get_round_matchs(self, roster)
        return self.round_matchs_list

    def get_already_played(self, roster):
        return gsheet.get_already_played(self, roster)

    def get_new_registrations_list(self):
        old = len(self.registrations_teams_list)
        self.registrations_teams_list = gsheet.get_registrations(self)
        response = []
        for x in self.registrations_teams_list:
            if old < x['ewb_ID']:
                response.append(x)
        if len(response) == 0 :
            response = False
        return response
    
    # def check_registrations_data(self):
    #     self.registrations_teams_list = gsheet.get_registration(self)
    #     for team in self.registrations_teams_list:
    #         print(team)
    
    def get_current_round_on_sheet(self):
        return gsheet.get_round_on_sheet(self)
    
    def get_last_row_on_players_data(self):
        row = gsheet.get_last_row_on_players_data(self)
        row = int(row.row + 1)
        return row
    
    def get_last_row_on_calc(self, roster):
        # def get_last_row_on_calc(self, roster):
        row = gsheet.get_last_row_on_calc(self, roster)
        row = int(row.row + 1)
        return row
    
    def get_match_row_for_score(self, roster, search):
        row = gsheet.get_last_calc_data(self, roster, search)
        return row
    
    def set_players_teams_list(self, target, data):
        return gsheet.set_data_players_to_sheet(self, target, data)
    
    def set_score_data(self, roster, target, data):
        return gsheet.set_data_scores_to_sheet(self, roster, target, data)
    
    def set_team_validator(self, target, validator):
        return gsheet.set_validator_team_to_sheet(self, target, data)


    ## NEW
    def get_team_matchs(self, roster, team):
        response = []
        data = new_gsheet.get_all_calc_datas(self, roster)
        for index, row in data.iterrows():
            if row['ewb_TeamA'] == team or row['ewb_TeamB'] == team:
                if type(row['PERCENT']) == str:
                    percent = row['PERCENT'].replace(",",".")
                if type(row['PERCENT_OPP']) == str:
                    percent_opp = row['PERCENT_OPP'].replace(",",".")
                response.append(f"`J{row['ewb_Round']}`.`{row['ewb_TeamA'][:9]:>9}` `{percent:>4}%` **`{row['STARS']:>2}`** {emojis.vs} **`{row['STARS_OPP']:<2}`** `{percent_opp:<4}%` `{row['ewb_TeamB'][:9]:<9}`\n")
        return response
        
    def get_team_classement(self, roster, team):
        data = new_gsheet.get_all_calc_datas(self, roster)
        for index, row in data.iterrows():
            # clt_Place	clt_Equipe	clt_Joué	clt_V	clt_Pts	clt_Diff	clt_PercentOff	clt_MoyStarsOff
            if row['clt_Equipe'] == team or row['clt_Equipe'] == team:
                return f"**`{row['clt_Place']:>2}`.`{row['clt_Equipe']}` `{row['clt_Pts']:>2}`pts** | `{row['clt_V']:>1}`vict. | diff.{emojis.star}`{row['clt_Diff']:>2}`"

    def get_team_players(self, team, roster):
        response = []
        data = new_gsheet.get_all_players_data(self)
        o = 0
        for index, row in data.iterrows():
            # ewb_PLayerTag	eb_PlayerTeam	ewb_PlayerName
            if row['ewb_PlayerTeam'] == team:
                print(roster)
                if row['ewb_PlayerRoster'] == roster:
                    o = o + 1
                    response.append(f"`{o}`. `{row['ewb_PlayerTag']:>10}` **{row['ewb_PlayerName']}**\n")
        return response

    def get_player_by_tag(self, tag):
        data = new_gsheet.get_all_players_data(self)
        response = []
        print(tag)
        for index, row in data.iterrows():
            if row['ewb_PlayerTag'] == tag:
                response.append(f"`{row['ewb_PlayerTag']:>10}` **{row['ewb_PlayerName']}** a joué pour **{row['ewb_PlayerTeam']}** en **{row['ewb_PlayerRoster']}**\n")
        if len(response) == 0:
            return f"Pas de résultat pour {tag}"
        else:
            return response
    
# CLASS ENFANTS
class Ranking(TournamentsManager):
    def __init__(self):
        self.instantiate_tournament()

class Ecup(TournamentsManager):
    def __init__(self):
        self.instantiate_tournament()

class Ecl(TournamentsManager):
    def __init__(self):
        self.instantiate_tournament()

if __name__ == "__main__":
    print(f"[ewb] Not for this use")
