
async def search_referent(self, ctx, search):
    search = ' '.join(search)
    finded = []
    print(search)
    for discord_user in self.ewb.get_all_members():
        # print(type(discord_user))
        if str(discord_user).lower() in str(search).lower() or str(search).lower() in str(discord_user).lower():
            if discord_user not in finded:
                finded.append(discord_user)
        else:
            pass
    print(len(finded))
    if len(finded) > 1:
        return finded
    else:
        return finded
    print(finded)
    return finded
