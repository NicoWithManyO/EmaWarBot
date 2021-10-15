
import pandas as pd

def get_round_on_sheet(self):
    return int(self.config_file.round_wk.acell('A1').value)
    

def get_registrations(self):
    response = []
    data = pd.DataFrame(self.config_file.import_wk.get_all_records())
    for index, row in data.iterrows():
        if row['ewb_Roster'] != "":
            response.append(row)
    return response

def get_round_matchs(self, roster):
    response = []
    data_mixt = pd.DataFrame(self.config_file.calc_mixt.get_all_records())
    data_full = pd.DataFrame(self.config_file.calc_full.get_all_records())
    if roster == "mixt":
        for index, row in data_mixt.iterrows():
            if row['ewb_TeamB'] != "":
                response.append(row)
    if roster == "full":
        for index, row in data_full.iterrows():
            if row['ewb_TeamB'] != "":
                response.append(row)
    return response

def set_data_team_to_sheet(self, target, data):
    return self.config_file.import_wk.update(target, data)

def set_data_tos_to_sheet(self, target, data):
    return self.config_file.tos_wk.update(target, data)

def set_data_players_to_sheet(self, target, data):
    return self.config_file.players_wk.update(target, data)

def get_last_row_on_players_data(self):
    return self.config_file.players_wk.find("ewb_last")

def get_last_calc_data(self, roster, search):
    if roster == "Mixt":
        return self.config_file.calc_mixt.find(search)
    if roster == "Full":
        return self.config_file.calc_full.find(search)


def set_data_scores_to_sheet(self, roster, target, data):
    if roster == "Mixt":
        return self.config_file.calc_mixt.update(target, data)
    if roster == "Full":
        return self.config_file.calc_full.update(target, data)