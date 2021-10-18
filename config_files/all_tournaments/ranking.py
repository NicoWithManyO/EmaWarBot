
import discord
import config_files.external_connectors.gsheet as sheet_config

code_name = "ranking"
name = code_name.title()
state = "active"
registrations_is_open = True
current_season = 20
current_round = 1
tournament_avatar = "https://media.discordapp.net/attachments/376111266521153538/608249950425317377/LogoRanking2.0_1.png?width=611&height=593"
date = "du 15/10/21 au 26/11/21"
start_date = "15/10/2021"

emo = "🔶"
referent_role = "🔶+Référent Ranking"
season_role = f"🔶+s20"
color = discord.Color.dark_green()

registration_recap_msg = None

rules = "https://s.divlo.fr/emaReglementRanking"
suivi_file = "https://s.divlo.fr/emaSuiviRanking"
engine_file = "https://docs.google.com/spreadsheets/d/11yRJt19xzpkBw--eFP0Wd6Ld9Iql3Lg4fDrSG8vR4OM/edit#gid=0"
import_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("NEW_VALIDATOR")
tos_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("data_tos")
calc_mixt = sheet_config.id_gs.open_by_url(engine_file).worksheet("calc_MIXT")
calc_full = sheet_config.id_gs.open_by_url(engine_file).worksheet("calc_FULL")
round_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("tempOTrick")
players_wk = sheet_config.id_gs.open_by_url(engine_file).worksheet("datas_players")


suivi_link = f""
liens_utiles = f"[Fichier de suivi](https://s.divlo.fr/emaSuiviRanking) | [Règlement](https://s.divlo.fr/emaReglementRanking) | **[Inscriptions](http://s.divlo.fr/emaInscriptionRanking)**\n[Calendrier](https://s.divlo.fr/CalendrierEma) | [Invite Discord](https://discord.gg/4yAZ2wV) | [Twitter Ema](https://twitter.com/emagine_gaming?lang=fr)"

translate_links = f"[🇬🇧 English Rules](https://s.divlo.fr/emaRankingRules_ENG) | [🇪🇦 Spanish Reglas](https://s.divlo.fr/emaRankingReglas_ESP)"

description = f"\n**Inscription du lundi au jeudi** à 20h pour la journée à venir\nTirage au sort : Jeudi soir après la clôture des inscriptions\nMatch : vendredi soir\n\n> **Inscriptions à renouveler chaque semaine : [Inscriptions](http://s.divlo.fr/emaInscriptionRanking)**\n\nQualification pour l'ECL & points pour le Master Clash\n\n> Retrouvez les planning, scores & classements dans le fichier de suivi"