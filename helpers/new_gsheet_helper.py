
import pandas as pd

def get_all_calc_datas(self, roster):
    if roster == "mixt":
        data = pd.DataFrame(self.config_file.calc_mixt.get_all_records())
    if roster == "full":
        data = pd.DataFrame(self.config_file.calc_full.get_all_records())
    return data

def get_all_players_data(self):
    response = []
    return pd.DataFrame(self.config_file.players_wk.get_all_records())
