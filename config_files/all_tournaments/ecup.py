
import discord
import config_files.external_connectors.gsheet as sheet_config

code_name = "ecup"
name = code_name.title()
state = "active"
registrations_is_open = False
current_season = 8
current_round = 1
tournament_avatar = "https://media.discordapp.net/attachments/720014731062280274/882319092227383296/Emagine_Cup-1.png?width=582&height=616"
date = "du 17/10/21 au 28/11/21"
start_date = "17/10/2021"

emo = "🔘"
referent_role = "🔘+Référent Ecup"
season_role = f"🔘+s{current_season}"
color = discord.Color.blue()

registration_recap_msg = None

suivi_file = "https://s.divlo.fr/emaSuiviECup"
engine_file = "https://docs.google.com/spreadsheets/d/1QNRBLXf1VpHakdO3x1_-qd5gZKH4QgqHuP4O8mCl8ig/edit#gid=1933450451"
import_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("VALIDATOR")
validaded_teams_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("ewb_TeamsExport")
calc_mixt = sheet_config.id_gs.open_by_url(engine_file).worksheet("calc_MIXT")
calc_full = sheet_config.id_gs.open_by_url(engine_file).worksheet("calc_FULL")
round_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("tempOTrick")
