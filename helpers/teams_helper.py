
import config_files.organization as orga
import helpers.gsheet_helper as gsheet_helper

async def search_referent(self, search):
    # search = ' '.join(search)
    finded = []
    for discord_user in orga.ema_guild.members:
        if str(discord_user).lower() in str(search).lower() or str(search).lower() in str(discord_user).lower() :
            if discord_user not in finded:
                finded.append(discord_user)
        else:
            pass
    return finded


async def search_discord_user(self, querry):
    matched = []
    for discord_user in self.ewb.get_all_members():
        if str(discord_user).lower() in str(querry).lower() or str(querry).lower() in str(discord_user).lower() or str(querry).lower() in str(discord_user.display_name).lower() or str(discord_user.display_name).lower() in str(querry).lower():
            if discord_user not in matched:
                matched.append(discord_user)
    return matched