import disnake
from disnake.ext import commands
import asyncio

TARGET_GUILD_IDS = [1191694936723161159]
TARGET_CHANNEL_IDS = [1236748500755152896, 1340619263072927784]


class JoinPinger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.member_queue = []
        self.processing_task = None

    @commands.Cog.listener()
    async def on_member_join(self, member: disnake.Member):
        if member.guild.id not in TARGET_GUILD_IDS:
            return

        self.member_queue.append(member)

        if self.processing_task is None or self.processing_task.done():
            self.processing_task = self.bot.loop.create_task(self.process_queue())

    async def process_queue(self):
        await asyncio.sleep(2)

        if not self.member_queue:
            return

        members_to_ping = self.member_queue.copy()
        self.member_queue.clear()

        pings_string = " ".join([member.mention for member in members_to_ping])

        for channel_id in TARGET_CHANNEL_IDS:
            channel = self.bot.get_channel(channel_id)

            if channel is None:
                print(f"[WARNING] Channel with ID {channel_id} not found.")
                continue

            if channel.guild.id not in TARGET_GUILD_IDS:
                continue

            try:
                message = await channel.send(pings_string)
                await message.delete()
                print(
                    f"[INFO] Pings for {len(members_to_ping)} users sent to channel {channel.name}"
                )
            except disnake.Forbidden:
                print(
                    f"[ERROR] The bot does not have permissions to send/delete messages in channel {channel.name} ({channel.id})"
                )
            except Exception as e:
                print(
                    f"[ERROR] An error occurred while sending pings to channel {channel.id}: {e}"
                )


def setup(bot: commands.Bot):
    bot.add_cog(JoinPinger(bot))
    print("[INFO] Cog 'AutoPing' loaded.")