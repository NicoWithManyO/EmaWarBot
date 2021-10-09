
import discord, os
from discord.ext import commands

import config_files.external_connectors.coc_api as coc_api

import config_files.ewb_bot as ewb_config

import helpers.boot_helper as boot_helper

class Daemon(commands.Bot):
    def __init__(self):
        print("[ewb] > starting ...")
        # boot discord option
        super().__init__(description = ewb_config.description,
                    intents = ewb_config.intents,
                    command_prefix = ewb_config.prefix,
                    case_insensitive = ewb_config.case_insensitive)
        
    async def on_ready(self):
        # boot sequence
        await boot_helper.set_running_env(self)
        await boot_helper.get_cogs_list_from_dir(self)
        await boot_helper.load_cogs_list(self)
        # coc api
        self.coc = coc_api.coc_client
        # OK
        print(f"[ewb] > I'm ready on {self.user}\n[ewb] > with prefix {' / '.join(ewb_config.prefix)}")


# starter
if __name__ == "__main__":
    ewb = Daemon()
    if os.environ.get("DEV_DISCORD_TOKEN"):
        ewb.run(os.environ.get("DISCORD_TOKEN"))
    else:
        import localtoken
        ewb.run(localtoken.ewb_token_dev)
