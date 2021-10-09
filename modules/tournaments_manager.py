

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
        # self.teams_list = gsheet.get_registrations(self)
        # self.date = config_file.date
        # self.final_teams_list = []
        
    def __str__(self):
        return f"{self.emo} **{self.name}** s{self.current_season}\nRound : {current_round}"

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