
import pandas as pd

def get_registrations(self):
    response = []
    data = pd.DataFrame(self.config_file.import_wk.get_all_records())
    for index, row in data.iterrows():
        if row['ewb_Roster'] != "":
            response.append(row)
    return response

def get_validaded_teams_list(self):
    response = []
    data = pd.DataFrame(self.config_file.validaded_teams_wk.get_all_records())
    for index, row in data.iterrows():
        if row['ewb_Roster'] != "":
            response.append(row)
    return response

def set_data_team_to_sheet(self, target, data):
    return self.config_file.import_wk.update(target, data)