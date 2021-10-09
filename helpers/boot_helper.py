
import os

import config_files.ewb_bot as ewb_config

async def set_running_env(self):
    if os.environ.get("DEV_DISCORD_TOKEN"):
        print(f"[ewb] > set remote env : Heroku")
        ewb_config.running_env = "remote_env"
    else:
        print(f"[ewb] > set local env")
        ewb_config.running_env = "local_env"
    return ewb_config.running_env

async def get_cogs_list_from_dir(self):
    ewb_config.cogs_to_load = []
    ewb_config.cogs_list = []
    for cog in os.listdir(ewb_config.cogs_dir):
        cog = cog.replace("__pycache__", "")
        cog = cog.replace(".py", "")
        if cog:
            ewb_config.cogs_to_load.append(f"{ewb_config.cogs_dir}.{cog}")
            ewb_config.cogs_list.append(f"{cog}")
    print(f"[ewb] > set cogs list from \"/{ewb_config.cogs_dir}/\"")
    return ewb_config.cogs_to_load

async def load_cogs_list(self):
    for cog in ewb_config.cogs_to_load:
        try:
            self.unload_extension(cog)
        except:
            pass
        self.load_extension(cog)
        print(f"[ewb] > {cog} loaded")
