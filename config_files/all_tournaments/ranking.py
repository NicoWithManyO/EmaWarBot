
import discord
import config_files.external_connectors.gsheet as sheet_config

code_name = "ranking"
name = code_name.title()
state = "active"
registrations_is_open = True
current_season = 20
current_round = 1
tournament_avatar = "https://cdn.discordapp.com/attachments/607932896526991366/749159353382207498/LogoRanking2.0.png"
date = "du 15/10/21 au 26/11/21"
start_date = "15/10/2021"

emo = "🔶"
referent_role = "🔶+Référent Ranking"
season_role = f"🔶+s20"
color = discord.Color.dark_green()

registration_recap_msg = None

suivi_file = ""
engine_file = "https://docs.google.com/spreadsheets/d/11yRJt19xzpkBw--eFP0Wd6Ld9Iql3Lg4fDrSG8vR4OM/edit#gid=0"
import_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("VALIDATOR")
tos_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("data_tos")