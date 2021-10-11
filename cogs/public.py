
import discord
from discord.ext import commands
from discord.ext import tasks

import config_files.emojis as emojis

import helpers.templates_to_publish as templates

# bot = discord.Bot()

class Public(commands.Cog):
    def __init__(self, ewb):
        self.ewb = ewb

    @commands.command(aliases = ["infos"])
    async def info(self, ctx, querry):
        """Retourne les informations connues sur l'élément donné
        
        Fournir un rôle, un membre, pour en avoir les informations
        - ema.info @NicoWithManyO#8020
        - ema.info @🔘+Référent Ecup
        """
        role = None
        member = None
        querry = querry.replace("<@!","").replace("<@&","").replace(">","").replace("<#","")
        role = discord.utils.get(ctx.guild.roles,id=int(querry))
        if role:
            desc = f"{len(role.members)} membre(s) | Mentionable : {role.mentionable}\nCréé le {str(role.created_at)[:10]}\nid:{role.id}"
            author = f"{type(role)}"
            title = f"{role}"
            logo = None
        else:
            member = discord.utils.get(ctx.guild.members,id=int(querry))
            if member:
                roles = []
                bot = ""
                
                if member.bot:
                    bot = emojis.system
                for x in member.roles:
                    roles.append(x.name)
                title = f"{bot} {member.display_name}"
                logo = member.avatar_url
                desc = f"Rôle(s) : {', '.join(roles)}\nDiscord depuis : {str(member.created_at)[:10]}\nMembre ici depuis : {str(member.joined_at)[:10]}\nid:{member.id}"
                author = f"{type(member)}"
        
        await ctx.send(embed = templates.create_std_embed(self, ctx, title = f"{title}", desc = f"{desc}", author = f"{author}", logo = logo))


def setup(bot):
    bot.add_cog(Public(bot))
