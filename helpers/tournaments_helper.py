
def select_tournament(self, cmd):
    if cmd.startswith("ecup."):
        return self.ewb.ecup
    if cmd.startswith("ecl."):
        return self.ewb.ecl
    if cmd.startswith("rkg") or cmd.startswith("ranking"):
        return self.ewb.ranking

def teams_selector(self, querry, data, author):
    to_show = []
    if querry == None:
        for team in data:
            if team['ewb_Ref1'] in str(author) or str(author) in team['ewb_Ref1']:
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
        