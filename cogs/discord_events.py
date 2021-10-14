
import discord
from discord.ext import commands
from discord.utils import get



import config_files.ewb_bot as ewb_config
import data.watched_id_list as watched_id_list
import config_files.emojis as emojis
import helpers.templates_to_publish as templates
import cogs.bot_admin as bot_admin
import helpers.translator_helper as translator_helper

class DiscordEvents(commands.Cog):
    """Description"""
    def __init__(self, ewb):
        self.ewb = ewb
        auto_role_channel = ewb.get_channel(ewb_config.temp)
        channel_to_log = ewb.get_channel(ewb_config.server_log_channel)

        @ewb.event
        async def on_member_update(before, after):
            role = ''
            action = ''
            if len(before.roles) < len(after.roles):
                role = next(role for role in after.roles if role not in before.roles)
                action = f"{emojis.add}"
            if len(before.roles) > len(after.roles):
                role = next(role for role in before.roles if role not in after.roles)
                action = f"{emojis.remove}"
            if role:
                await channel_to_log.send(f"`[ewb]` {action} `{role}` {emojis.right_arrow} `{after}`")

        @ewb.event
        async def on_member_join(member):
            counter = 0
            with open("data/temp/entry.txt", "r+") as file:
                counter = counter + 1
                file.write(f"{str(member.id)}\n" )
                if counter > int(ewb_config.limit_raid_detect):
                    bot_admin.lock_server(self)
                    await channel_to_log.send(f"`[ewb]` + **Le serveur est lock** {ewb_config.lock}")
            await channel_to_log.send(f"[ewb] **+ {member.mention}** ({member.id}) à rejoint le serveur")
            if member.id in watched_id_list.id_list:
                await channel_to_log.send(f"[ewb] **! {member.mention}** ({member.id}) est dans la liste des id surveillés ! @NicoWithManyO | Staff E-magine#8020")
                return
            else:
                if ewb_config.lock == False:
                    guild = ewb.get_guild(member.guild.id)
                    role = discord.utils.get(guild.roles, name="_o")
                    await member.add_roles(role)
                    await channel_to_log.send(f"`[ewb]` **+ rôle {role} {member}** ({member.id})")
                else:
                    await channel_to_log.send(f"`[ewb]` ! {member} le serveur est actuellement lock")
        
        @ewb.event
        async def on_member_remove(member):
            await channel_to_log.send(f"`[ewb]` **- {member}** ({member.id}) à quitté le serveur")        
        
        @ewb.event
        async def on_message(message):
            if message.author == ewb or message.author.id == 273538058731651102 or message.author.id == 715163285523267606 or message.author.id == 755884056159191050:
                return
            counter = 0
            with open("data/temp/spam.txt", "r+") as file:
                for lines in file:
                    if lines.strip("\n") == str(message.author.id):
                        counter = counter + 1
                file.write(f"{str(message.author.id)}\n" )
                if counter > int(ewb_config.limit_spam_detect):
                    try:
                        await channel_to_log.send(f"`[ewb]` **/!\ Spam détecté {message.author.mention}** ({message.author.id}) dans #{message.channel}")
                        await message.author.edit(roles=[])
                    except:
                        await channel_to_log.send(f"`[ewb]` /!\ Spam détecté {message.author.mention} ({message.author.id}) dans #{message.channel}\n**Droit insuffisant pour intervenir !**")
            await ewb.process_commands(message)
        
        @ewb.event
        async def on_raw_message_delete(before):
            if not before.author.bot:
                await channel_to_log.send(f"`[ewb]` `{before.channel_id}` {emojis.remove} ")
        
        @ewb.event
        async def on_message_edit(before, after):
            if not before.author.bot:
                await channel_to_log.send(f"`[ewb]` `{before.channel}` {emojis.remove} `{before.author}` {emojis.right_arrow} ~~`{before.content}`~~")

        @ewb.event
        async def on_raw_reaction_add(payload):
            role = None
            role_to_remove = None
            guild = ewb.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            
            
            if payload.message_id == ewb_config.welcome_valid_message:
                if str(payload.emoji) == emojis.valid:
                    guild = ewb.get_guild(payload.guild_id)
                    role = discord.utils.get(guild.roles, name="Membre")
                    role_to_remove = discord.utils.get(guild.roles, name="_o")
                    if member not in role.members:
                        pass
                        # await channel_to_log.send(content = f"{member.mention}", embed = await templates.standard_head_embed(self, tiny = True, title = f"Bienvenue **{member.display_name}**", desc = "Le Staff E-magine est ravi de t'accueillir parmi nous et reste à ta disposition ...\n\nPour ne rien rater, nous te conseillons de :\n> suivre notre room d'annonce\n> suivre [le Twitter Ema](https://twitter.com/emagine_gaming?lang=fr)", pic_url = member.avatar_url))
            if payload.message_id == ewb_config.language_selector_message:
                if str(payload.emoji) == emojis.en:
                    role = discord.utils.get(guild.roles, name="🇬🇧 (en)")
                if str(payload.emoji) == emojis.es:
                    role = discord.utils.get(guild.roles, name="🇪🇸 (es)")
                if str(payload.emoji) == emojis.de:
                    role = discord.utils.get(guild.roles, name="🇩🇪 (de)")
                if str(payload.emoji) == emojis.hi:
                    role = discord.utils.get(guild.roles, name="🇮🇳 (hi)")
            if payload.message_id == ewb_config.th_selector_message:
                if str(payload.emoji) == emojis.th11:
                    role = discord.utils.get(guild.roles, name="HdV 11")
                if str(payload.emoji) == emojis.th12:
                    role = discord.utils.get(guild.roles, name="HdV 12")
                if str(payload.emoji) == emojis.th13:
                    role = discord.utils.get(guild.roles, name="HdV 13")
                if str(payload.emoji) == emojis.th14:
                    role = discord.utils.get(guild.roles, name="HdV 14")
            if role:
                await member.add_roles(role)
                # await channel_to_log.send(f"`[ewb]` + rôle {role} **{member}** ({member.id})")
            if role_to_remove:
                await member.remove_roles(role_to_remove)
                # await channel_to_log.send(f"`[ewb]` - rôle {role_to_remove} **{member}** ({member.id})")

        @ewb.event
        async def on_raw_reaction_remove(payload):
            role = None
            role_to_add = None
            guild = ewb.get_guild(payload.guild_id)
            member = guild.get_member(payload.user_id)
            if payload.message_id == ewb_config.language_selector_message:
                if str(payload.emoji) == emojis.en:
                    role = discord.utils.get(guild.roles, name="🇬🇧 (en)")
                if str(payload.emoji) == emojis.es:
                    role = discord.utils.get(guild.roles, name="🇪🇸 (es)")
                if str(payload.emoji) == emojis.de:
                    role = discord.utils.get(guild.roles, name="🇩🇪 (de)")
                if str(payload.emoji) == emojis.hi:
                    role = discord.utils.get(guild.roles, name="🇮🇳 (hi)")
            if payload.message_id == ewb_config.th_selector_message:
                if str(payload.emoji) == emojis.th11:
                    role = discord.utils.get(guild.roles, name="HdV 11")
                if str(payload.emoji) == emojis.th12:
                    role = discord.utils.get(guild.roles, name="HdV 12")
                if str(payload.emoji) == emojis.th13:
                    role = discord.utils.get(guild.roles, name="HdV 13")
                if str(payload.emoji) == emojis.th14:
                    role = discord.utils.get(guild.roles, name="HdV 14")
            if payload.message_id == ewb_config.welcome_valid_message:
                if str(payload.emoji) == emojis.validFixed:
                    role = discord.utils.get(guild.roles, name="Membre")
                    role_to_add = discord.utils.get(guild.roles, name="_o")
            if role:
                await member.remove_roles(role)
                # await channel_to_log.send(f"`[ewb]` - {role} **{member}** ({member.id})")
            if role_to_add:
                await member.add_roles(role_to_add)
                # await channel_to_log.send(f"`[ewb]` + {role_to_add} **{member}** ({member.id})")

        @ewb.event
        async def on_reaction_add(reaction, user):
            channel_to_translate = ewb.get_channel(reaction.message.channel.id)
            if reaction.message.id == ewb_config.language_selector_message:
                return
            target_language = None
            if str(user) != "ManyO_emaWarBot#4034" and str(user) !="emaWarBoOOoOot#4184":
                if str(reaction.emoji) == emojis.en_publish:
                    channel_to_translate = ewb.get_channel(ewb_config.temp_en_announcement)
                    target_language = "en"
                if str(reaction.emoji) == emojis.publish:
                    channel_to_translate = ewb.get_channel(ewb_config.temp_announcement)
                    await channel_to_translate.send(f"{reaction.message.content}")
                    return
                if str(reaction.emoji) == emojis.fr:
                    target_language = "fr"
                if str(reaction.emoji) == emojis.en:
                    target_language = "en"
                if str(reaction.emoji) == emojis.es:
                    target_language = "es"
                if str(reaction.emoji) == emojis.de:
                    target_language = "de"
                if str(reaction.emoji) == emojis.hi:
                    target_language = "hi"
                if len(reaction.message.content) < 2:
                    to_translate = reaction.message.embeds[0].description.replace(emojis.down, "")
                    response = translator_helper.translate_data(target_language, to_translate)
                    await channel_to_translate.send(embed = await templates.standard_head_embed(self, tiny = True, desc = f"{reaction.emoji}\t{str(response.text.replace('<@! ', '<@!').replace('<# ', '<#').replace('<@ ','<@').replace('<@& ','<@'))}"))
                    return
                else:
                    to_translate = reaction.message.content
                if target_language:
                    response = translator_helper.translate_data(target_language, to_translate)
                    await channel_to_translate.send(f"[ewb] Message ({response.src}) from {reaction.message.author.display_name} translated into {reaction.emoji} ({response.dest})\n{response.text.replace('<@! ', '<@!').replace('<# ', '<#').replace('<@ ','<@').replace('<@& ','<@&')}")

def setup(bot):
    bot.add_cog(DiscordEvents(bot))
