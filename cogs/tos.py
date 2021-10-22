
import discord
from discord.ext import commands

import random

import helpers.tournaments_helper as tournaments_helper
import helpers.gsheet_helper as gsheet
import config_files.emojis as emojis


def is_rematch(current_match, already):
    if f"{current_match[0]}/{current_match[1]}" in already or f"{current_match[1]}/{current_match[0]}" in already:
        print(f"rematch {current_match[0]} {current_match[1]}")
        return True
    else:
        return False
    
def write_tos(tos, roster, exempt, tournament):
    if roster.lower() == "mixt":
        target = f"O1"
        target_exempt = f"Q1"
    if roster.lower() == "full":
        target = f"X1"
        target_exempt = f"Z1"
    if exempt:
        print(gsheet.set_data_tos_to_sheet(tournament, target_exempt, exempt))
    return gsheet.set_data_tos_to_sheet(tournament, target, tos)

def write_tos_to_calc(tos, roster, exempt, tournament):
    if roster.lower() == "mixt":
        target = f"O1"
        target_exempt = f"Q1"
    if roster.lower() == "full":
        target = f"X1"
        target_exempt = f"Z1"
    return gsheet.set_data_tos_to_sheet(tournament, target, tos)

class Tos(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb


    @commands.command()
    # @commands.has_role("Staff E-magine ⭐")
    async def newTos(self, ctx, roster, troll=None):
        final_teams_list = []
        matchs_list = []
        exempt = ""
        tournament = tournaments_helper.select_tournament(self, ctx.message.content)
        data = tournament.get_registrations_teams_list()
        already_played_matchs = tournament.get_already_played(roster)
        for team in data:
            if team['ewb_Roster'].lower() == roster.lower():
                if team['ewb_FinalState'] == "Validée":
                    final_teams_list.append(f"{team['ewb_NomEquipe']}")
        await ctx.send(f"Matchs déjà joués : {' `|` '.join(already_played_matchs[::2])}")
        await ctx.send(f"**`{roster}` {len(final_teams_list)} équipes : {' `|` '.join(final_teams_list)}**")
        message = await ctx.send(f"```Tirage au sort {roster} {tournament}```")
        nbre_teams = len(final_teams_list)
        
        already = []
        for x in already_played_matchs:            
            already.append(x[:-2])
        print(already)
        print(final_teams_list)

        while len(final_teams_list) > 1:
        # if rematch:
        #     original_list = save_original_list
            
            print(len(final_teams_list))

            current = random.sample(final_teams_list, 2)
            if not is_rematch(current, already):
                print(f"ok {current}")
                matchs_list.append(current)
                final_teams_list.remove(current[0])
                final_teams_list.remove(current[1])
            else:
                await ctx.send(f"> [ewb] Rematch {' `vs` '.join(current)} ({len(matchs_list)}). Restart")
                if matchs_list:
                    for x in matchs_list:
                        for y in x:
                            if y not in final_teams_list:
                                final_teams_list.append(y)
                    matchs_list = []
            
        print(matchs_list)
        o = 0
        for x in matchs_list:
            o = o + 1
            await ctx.send(f"`{o}`. **{'** `vs` **'.join(x)}**")
        if final_teams_list:
            await  ctx.send(f"**{final_teams_list[0]}** est exempt")
            print(final_teams_list[0])
            exempt = final_teams_list[0]
        
        while True:
            reaction = await addiing(message)
            # reaction = await self.ewb.wait_for_reaction(emoji="{emojis.mixt}", message=message)
            await ctx.send(write_tos(matchs_list, roster, exempt, tournament))
            await ctx.send("ok. fin")

def setup(bot):
    bot.add_cog(Tos(bot))
