

import config_files.all_tournaments.ecup as ecup_config
import config_files.all_tournaments.ranking as ranking_config
import config_files.all_tournaments.ecl as ecl_config

import helpers.gsheet_helper as gsheet

import config_files.emojis as emojis

def get_registrations_list(self):
    self.registrations_list = gsheet.get_registrations_list(self)
    return self.registrations_list


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
        self.current_round = config_file.current_round
        self.config_file = config_file
        self.tournament_avatar = config_file.tournament_avatar
        
        self.current_registrations_number = 0
        self.validaded_teams_list = None
        self.registrations_teams_list = gsheet.get_registrations(self)
        
    def __str__(self):
        return f"{self.emo} {self.name} {emojis.current_season}{self.current_season} | {emojis.current_round}{self.current_round}"

    def get_registrations_teams_list(self):
        self.registrations_teams_list = gsheet.get_registrations(self)
        return self.registrations_teams_list

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

    def check_all_referents(self):
        self.registrations_teams_list = gsheet.get_registrations(self)
        for x in self.registrations_teams_list:
            print(x)
            
        
        
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