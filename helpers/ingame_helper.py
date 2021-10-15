
import coc

async def check_clan_tag(self, tag):
    if tag:
        tag = coc.utils.correct_tag(tag)
        try:
            clan = await self.ewb.coc.get_clan(tag)
            return clan
        except:
            return False



async def check_current_war(self, tag):
    if tag:
        tag = coc.utils.correct_tag(tag)
        try:
            war = await self.ewb.coc.get_current_war(tag)
            return war
        except coc.PrivateWarLog:
            return "close_warlog"
        
        if war is None:
            return "cwl"