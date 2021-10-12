
import coc

async def check_clan_tag(self, tag):
    if tag:
        tag = coc.utils.correct_tag(tag)
        try:
            clan = await self.ewb.coc.get_clan(tag)
            return clan
        except:
            return False