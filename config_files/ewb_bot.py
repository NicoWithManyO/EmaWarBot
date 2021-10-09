        # super().__init__(description = ewb_config.description,
        #             intents = ewb_config.intents,
        #             command_prefix = ewb_config.prefix,
        #             case_insensitive = ewb_config.case_insensitive)

import discord

# base options
prefix = ["dev.", "ecup.", "ranking.", "ecl."]
case_insensitive = True
intents = discord.Intents.all()
description = "EmaWarBot pour E-magine Gaming | NicoWithManyO#8020"

# boot options 
running_env = None
cogs_dir = "cogs"
