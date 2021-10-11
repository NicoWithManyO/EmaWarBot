
import discord
import config_files.external_connectors.gsheet as sheet_config

code_name = "ranking"
name = code_name.title()
state = "active"
registrations_is_open = True
current_season = 20
current_round = 1
tournament_avatar = "https://media.discordapp.net/attachments/720014731062280274/882319092227383296/Emagine_Cup-1.png?width=582&height=616"
date = "du 15/10/21 au 26/11/21"
start_date = "15/10/2021"

emo = "🔶"
referent_role = "🔶+Référent {name}"
season_role = f"🔶+s{current_season}"
color = discord.Color.dark_green()

suivi_file = ""
engine_file = "https://docs.google.com/spreadsheets/d/11yRJt19xzpkBw--eFP0Wd6Ld9Iql3Lg4fDrSG8vR4OM/edit#gid=0"
import_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("VALIDATOR")