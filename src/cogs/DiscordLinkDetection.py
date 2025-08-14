import re

from disnake.ext import commands


class DiscordLinkDetection(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.invite_pattern = re.compile(
            r"(?:https?://)?(?:www\.)?(?:discord\.(?:gg|io|me|li)|discordapp\.com/invite)/+[a-zA-Z0-9]+"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.guild_permissions.administrator:
            return

        if self.invite_pattern.search(message.content):
            await message.delete()
            msg = await message.channel.send(
                f"{message.author.mention}, no invite links, my dude!"
            )
            await msg.delete(delay=5)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        if after.author.guild_permissions.administrator:
            return

        if self.invite_pattern.search(after.content):
            await after.delete()
            msg = await after.channel.send(
                f"{after.author.mention}, no invite links, my dude!"
            )
            await msg.delete(delay=5)


class AntiDiscordAdvertising(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.discord_links = re.compile(
            r"(?:https?://)?(?:www\.)?(?:discord\.gg|discord\.com/invite|discordapp\.com/invite)"
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot:
            return

        if message.author.guild_permissions.administrator:
            return

        if self.discord_links.search(message.content):
            await message.delete()
            msg = await message.channel.send(
                f"{message.author.mention}, no advertising other Discords here!"
            )
            await msg.delete(delay=5)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        if after.author.bot:
            return

        if self.discord_links.search(after.content):
            await after.delete()
            msg = await after.channel.send(
                f"{after.author.mention}, no advertising other Discords here!"
            )
            await msg.delete(delay=5)


def setup(bot):
    print("[INFO] DiscordLinkDetection and AntiDiscordAdvertising loaded")
    bot.add_cog(DiscordLinkDetection(bot))
    bot.add_cog(AntiDiscordAdvertising(bot))