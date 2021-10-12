

def select_tournament(self, cmd):
    if cmd.startswith("ecup."):
        return self.ewb.ecup
    if cmd.startswith("ecl."):
        return self.ewb.ecl
    if cmd.startswith("rkg") or cmd.startswith("ranking"):
        return self.ewb.ranking