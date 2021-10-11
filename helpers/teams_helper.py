
import config_files.organization as orga

async def search_referent(self, search):
    # search = ' '.join(search)
    finded = []
    print(search)
    print(self.ewb.get_all_members)
    for discord_user in orga.ema_guild.get_all_members():
        # print(type(discord_user))
        if str(discord_user).lower() in str(search).lower() or str(search).lower() in str(discord_user).lower():
            if discord_user not in finded:
                finded.append(discord_user)
        else:
            pass
    print(f"o {finded}")
    return finded
