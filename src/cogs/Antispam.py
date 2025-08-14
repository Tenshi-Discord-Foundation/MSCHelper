import disnake
from disnake.ext import commands
import re
from collections import defaultdict
import time
from datetime import datetime, timedelta
import aiohttp


class Antispam(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.spam_threshold = 6
        self.spam_interval = 15
        self.message_counts = defaultdict(lambda: {"count": 0, "last_time": 0})

        self.duplicate_message_threshold = 6
        self.duplicate_message_interval = 15
        self.recent_messages = defaultdict(list)

        self.spotify_spam_threshold = 3
        self.spotify_spam_interval = 60
        self.spotify_message_counts = defaultdict(lambda: {"count": 0, "last_time": 0})

        self.spotify_regex = re.compile(
            r"https?://open\.spotify\.com/(track|album|playlist)/[a-zA-Z0-9]+"
        )

        self.webhook_url = (
            "https://discord.com/api/webhooks/1345383651860414525/"
            "aMcxpyc1uRDRTLS1Tv5TL1lStO_MJY0805egXdA1-Y2ghFTRNev"
            "_DJeO3SSfKxA3QXAq"
        )
        self.session = None
        self.webhook = None

    async def cog_load(self):
        self.session = aiohttp.ClientSession()
        self.webhook = disnake.Webhook.from_url(self.webhook_url, session=self.session)

    async def cog_unload(self):
        if self.session:
            await self.session.close()

    @commands.slash_command(
        name="set_spam_threshold",
        description="Set the limit for regular spam.",
    )
    @commands.has_permissions(administrator=True)
    async def set_spam_threshold(
        self,
        inter: disnake.ApplicationCommandInteraction,
        threshold: int = commands.Param(
            description="How many messages before it's spam.", gt=0, default=6
        ),
        interval: int = commands.Param(
            description="Time window in seconds.", gt=0, default=15
        ),
    ):
        self.spam_threshold = threshold
        self.spam_interval = interval
        await inter.response.send_message(
            f"✅ A'ight, spam limit is now `{threshold}` messages in `{interval}` seconds.",
            ephemeral=True,
        )

    @commands.slash_command(
        name="set_duplicate_threshold",
        description="Set the limit for copy-paste spam.",
    )
    @commands.has_permissions(administrator=True)
    async def set_duplicate_threshold(
        self,
        inter: disnake.ApplicationCommandInteraction,
        threshold: int = commands.Param(
            description="How many copy-pastes before it's spam.", gt=0, default=6
        ),
        interval: int = commands.Param(
            description="Time window in seconds.", gt=0, default=15
        ),
    ):
        self.duplicate_message_threshold = threshold
        self.duplicate_message_interval = interval
        await inter.response.send_message(
            f"✅ Gotcha, copy-paste limit is now `{threshold}` messages in `{interval}` seconds.",
            ephemeral=True,
        )

    @commands.slash_command(
        name="set_spotify_threshold",
        description="Set the limit for Spotify link spam.",
    )
    @commands.has_permissions(administrator=True)
    async def set_spotify_threshold(
        self,
        inter: disnake.ApplicationCommandInteraction,
        threshold: int = commands.Param(
            description="How many links before it's spam.", gt=0, default=3
        ),
        interval: int = commands.Param(
            description="Time window in seconds.", gt=0, default=60
        ),
    ):
        self.spotify_spam_threshold = threshold
        self.spotify_spam_interval = interval
        await inter.response.send_message(
            f"✅ Cool, Spotify link spam limit is now `{threshold}` links in `{interval}` seconds.",
            ephemeral=True,
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author.bot or message.guild is None:
            return

        if message.author.guild_permissions.administrator:
            return

        user_id = message.author.id
        current_time = time.time()

        if self.spotify_regex.search(message.content):
            await self.handle_spotify_link_spam(message, user_id, current_time)
            return

        if isinstance(message.activity, dict) and message.activity.get("type") == 3:
            await self.handle_spotify_rpc(message)
            return

        if message.embeds:
            if await self.handle_spotify_embed(message):
                return

        await self.handle_general_spam(message, user_id, current_time)
        await self.handle_duplicate_messages(message, user_id)

    async def handle_spotify_link_spam(self, message, user_id, current_time):
        spotify_user_data = self.spotify_message_counts[user_id]

        if current_time - spotify_user_data["last_time"] > self.spotify_spam_interval:
            spotify_user_data["count"] = 1
        else:
            spotify_user_data["count"] += 1

        spotify_user_data["last_time"] = current_time

        if spotify_user_data["count"] >= self.spotify_spam_threshold:
            await self.punish_user(message, "Spamming Spotify links")
            spotify_user_data["count"] = 0

    async def handle_spotify_rpc(self, message):
        await self.delete_message(message, "Spotify RPC")

    async def handle_spotify_embed(self, message):
        for embed in message.embeds:
            is_invite = "invites you to listen to Spotify"
            if embed.type == "rich" and (
                (embed.provider and embed.provider.name == "Spotify")
                or (embed.description and is_invite in embed.description)
                or (embed.title and is_invite in (embed.title or ""))
            ):
                await self.delete_message(message, "Spotify embed")
                return True
        return False

    async def handle_general_spam(self, message, user_id, current_time):
        user_data = self.message_counts[user_id]

        if current_time - user_data["last_time"] < self.spam_interval:
            user_data["count"] += 1
            if user_data["count"] >= self.spam_threshold:
                await self.punish_user(message, "Spamming messages too fast")
        else:
            user_data["count"] = 1
            user_data["last_time"] = current_time

    async def handle_duplicate_messages(self, message, user_id):
        message_content = message.content.strip().lower()
        now = datetime.now()

        self.recent_messages[message_content] = [
            (uid, ts)
            for uid, ts in self.recent_messages[message_content]
            if now - ts < timedelta(seconds=self.duplicate_message_interval)
        ]

        self.recent_messages[message_content].append((user_id, now))

        unique_users = set(uid for _, uid in self.recent_messages[message_content])

        if (
            len(self.recent_messages[message_content])
            >= self.duplicate_message_threshold
        ):
            uids_str = ", ".join([str(uid) for uid in unique_users])
            log_msg = (
                f"Duplicate message spam detected in "
                f"{message.channel.name} ({message.channel.id}). "
                f"Content: '{message_content}'. Members: {uids_str}"
            )
            await self.webhook.send(log_msg)

            for uid in unique_users:
                member = message.guild.get_member(uid)
                if member and not member.bot:
                    await self.punish_user(
                        message, "Spamming duplicate messages", member
                    )

            del self.recent_messages[message_content]

    async def punish_user(self, message, reason, member=None):
        if member is None:
            member = message.author

        try:
            await message.delete()
            log_msg = (
                f"Deleted message from {member} ({member.id}) in channel "
                f"{message.channel.name} ({message.channel.id}) "
                f"due to {reason}."
            )
            await self.webhook.send(log_msg)

            if not member.bot:
                await member.timeout(
                    until=datetime.now() + timedelta(minutes=5), reason=reason
                )
                log_msg = f"Timed out user {member} ({member.id}) for {reason}."
                await self.webhook.send(log_msg)
        except disnake.Forbidden:
            log_msg = (
                f"Failed to handle spam from {member} ({member.id}) "
                f"(no permissions)."
            )
            if self.webhook:
                await self.webhook.send(log_msg)
        except Exception as e:
            print(f"Error punishing user: {e}")

    async def delete_message(self, message, reason):
        try:
            await message.delete()
            log_msg = (
                f"Deleted message from {message.author} "
                f"({message.author.id}) in channel {message.channel.name} "
                f"({message.channel.id}) due to {reason}."
            )
            await self.webhook.send(log_msg)
        except disnake.Forbidden:
            print(f"Failed to delete message from {message.author} (no permissions).")
        except Exception as e:
            print(f"Error sending to webhook ({reason}): {e}")


def setup(bot):
    bot.add_cog(Antispam(bot))