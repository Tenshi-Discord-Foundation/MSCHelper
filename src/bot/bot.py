import os

import disnake
from disnake.ext import commands


class Bot(commands.Bot):
    def __init__(self):
        super().__init__(
            intents=disnake.Intents.all(),
            command_prefix=["!", "-"],
            case_insensitive=True,
        )
        base_dir = os.path.dirname(
            os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        )
        cogs_dir = os.path.join(base_dir, "src", "cogs")
        for file in os.listdir(cogs_dir):
            if file.endswith(".py"):
                print(f"Loading cog: {file}")
                self.load_extension(f"src.cogs.{file[:-3]}")
        print("All extensions loaded")
