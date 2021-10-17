
def select_tournament(self, cmd):
    cmd = cmd.lower()    
    if cmd.startswith("ecup."):
        return self.ewb.ecup
    if cmd.startswith("ecl."):
        return self.ewb.ecl
    if cmd.startswith("rkg") or cmd.startswith("ranking"):
        return self.ewb.ranking

def teams_selector(self, querry, data, search_author):
    to_show = []
    if querry == "":
        for team in data:
            if str(search_author) in team['ewb_Ref1'] or team['ewb_Ref1'] in str(search_author) or str(search_author) in team['ewb_Ref2']:
                to_show.append(team)
    else:
        try:
            querry = int(querry)
            for team in data:
                if team['ewb_ID'] == querry:
                    to_show.append(team)
        except:
            for team in data:
                if str(team['ewb_NomEquipe']).lower() in querry.lower() or querry.lower() in str(team['ewb_NomEquipe']).lower():
                    to_show.append(team)
    return to_show
        