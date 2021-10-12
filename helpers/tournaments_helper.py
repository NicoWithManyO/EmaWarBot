
def select_tournament(self, cmd):
    if cmd.startswith("ecup."):
        return self.ewb.ecup
    if cmd.startswith("ecl."):
        return self.ewb.ecl
    if cmd.startswith("rkg") or cmd.startswith("ranking"):
        return self.ewb.ranking

def teams_selector(self, querry, data, search_author):
    to_show = []
    if querry == None:
        print("none")
        for team in data:
            if team['ewb_Ref1'] in str(search_author) or team['ewb_Ref2'] in str(search_author):
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
        