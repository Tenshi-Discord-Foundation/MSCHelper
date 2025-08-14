import disnake
from disnake.ext import commands
import datetime
import re
import sys
import traceback
import sqlite3

MODERATOR_ROLE_IDS = [
    1191695072857686056,
    1321923616794742885,
    1398641721386078228,
    1341819110090211408,
]
APPROVER_ROLE_IDS = [1191695072857686056, 1321923616794742885, 1398641721386078228]
MODERATOR_ROLE_ID = 1341819110090211408

LOG_CHANNEL_ID = 1391354845272735856
STAFF_LOG_CHANNEL_ID = 1398649472363532348

DB_FILE = "moderation.db"


def parse_duration(duration_str: str) -> datetime.timedelta:
    """Parses a time string and returns a timedelta object."""
    match = re.match(r"(\d+)([smhd])", duration_str.lower())
    if not match:
        raise ValueError(
            "Invalid time format. Use 's', 'm', 'h', 'd'. For example: 10m, 2h, 1d."
        )

    value, unit = int(match.group(1)), match.group(2)

    if unit == "s":
        return datetime.timedelta(seconds=value)
    if unit == "m":
        return datetime.timedelta(minutes=value)
    if unit == "h":
        return datetime.timedelta(hours=value)
    if unit == "d":
        return datetime.timedelta(days=value)
    return None


class DenyReasonModal(disnake.ui.Modal):
    def __init__(self, original_message: disnake.Message, approver: disnake.Member):
        self.original_message = original_message
        self.approver = approver

        components = [
            disnake.ui.TextInput(
                label="Reason for denial",
                placeholder="Explain why you're denying this request...",
                custom_id="deny_reason_input",
                style=disnake.TextInputStyle.paragraph,
                required=True,
                max_length=500,
            )
        ]
        super().__init__(
            title="Reason for Ban Denial",
            components=components,
            custom_id="deny_reason_modal",
        )

    async def callback(self, inter: disnake.ModalInteraction):
        reason = inter.text_values["deny_reason_input"]

        original_content = self.original_message.content

        verdict_text = (f"**Verdict:** {self.approver.mention} (`{self.approver.id}`) "
                        f"denied the ban request. Reason: **{reason}**.")
        new_content = f"{original_content}\n- {verdict_text}"

        await self.original_message.edit(content=new_content, view=None)
        await inter.response.send_message(
            "Denial verdict has been successfully issued.", ephemeral=True
        )


class BanRequestView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    async def check_approver_role(self, inter: disnake.MessageInteraction) -> bool:
        user_role_ids = {role.id for role in inter.author.roles}
        if not user_role_ids.intersection(APPROVER_ROLE_IDS):
            await inter.response.send_message(
                "You don't have the right permissions for this action.", ephemeral=True
            )
            return False
        return True

    @disnake.ui.button(
        label="Approve",
        style=disnake.ButtonStyle.success,
        custom_id="ban_request_approve",
    )
    async def approve_button(
        self,
        button: disnake.ui.Button,
        inter: disnake.MessageInteraction,
    ):
        if not await self.check_approver_role(inter):
            return

        match = re.search(r"user <@!?(\d+)>", inter.message.content)
        if not match:
            await inter.response.send_message(
                "Couldn't find the user ID in the message.", ephemeral=True
            )
            return

        target_id = int(match.group(1))

        try:
            reason = f"Ban approved by moderator {inter.author.name} ({inter.author.id})"
            await inter.guild.ban(user=disnake.Object(id=target_id), reason=reason)

            original_content = inter.message.content

            verdict_text = f"**Verdict:** {inter.author.mention} (`{inter.author.id}`) approves the ban request."
            new_content = f"{original_content}\n- {verdict_text}"

            await inter.message.edit(content=new_content, view=None)
            await inter.response.send_message(
                "Ban request approved. The user has been banned.", ephemeral=True
            )

        except disnake.NotFound:
            await inter.response.send_message(
                "Couldn't find the user to ban. Maybe they already left the server.",
                ephemeral=True,
            )
        except disnake.Forbidden:
            await inter.response.send_message(
                "The bot doesn't have enough permissions to ban this user.",
                ephemeral=True,
            )
        except Exception as e:
            await inter.response.send_message(f"An error occurred: {e}", ephemeral=True)

    @disnake.ui.button(
        label="Deny",
        style=disnake.ButtonStyle.danger,
        custom_id="ban_request_deny",
    )
    async def deny_button(
        self,
        button: disnake.ui.Button,
        inter: disnake.MessageInteraction,
    ):
        if not await self.check_approver_role(inter):
            return

        modal = DenyReasonModal(original_message=inter.message, approver=inter.author)
        await inter.response.send_modal(modal)



class UnifiedModerationCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.view_added = False

        self.conn = sqlite3.connect(DB_FILE)
        self.cursor = self.conn.cursor()
        self._setup_database()

    def _setup_database(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS reprimands (
                user_id INTEGER PRIMARY KEY,
                count INTEGER NOT NULL DEFAULT 0
            )
        """
        )
        self.conn.commit()
        print("[INFO] Database for reprimands is ready.")

    def _get_reprimands(self, user_id: int) -> int:
        self.cursor.execute(
            "SELECT count FROM reprimands WHERE user_id = ?", (user_id,)
        )
        result = self.cursor.fetchone()
        return result[0] if result else 0

    def _add_reprimand(self, user_id: int) -> int:
        current_count = self._get_reprimands(user_id)
        new_count = current_count + 1
        self.cursor.execute(
            """
            INSERT INTO reprimands (user_id, count) VALUES (?, ?)
            ON CONFLICT(user_id) DO UPDATE SET count = ?
        """,
            (user_id, new_count, new_count),
        )
        self.conn.commit()
        return new_count

    def _remove_reprimand(self, user_id: int) -> int:
        current_count = self._get_reprimands(user_id)
        new_count = max(0, current_count - 1)
        self.cursor.execute(
            "UPDATE reprimands SET count = ? WHERE user_id = ?", (new_count, user_id)
        )
        self.conn.commit()
        return new_count

    def _reset_reprimands(self, user_id: int):
        self.cursor.execute(
            "UPDATE reprimands SET count = 0 WHERE user_id = ?", (user_id,)
        )
        self.conn.commit()

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.view_added:
            self.bot.add_view(BanRequestView())
            self.view_added = True
            print("[INFO] Persistent view 'BanRequestView' registered.")

    @commands.Cog.listener()
    async def on_slash_command_error(
        self,
        inter: disnake.ApplicationCommandInteraction,
        error: commands.CommandError,
    ):
        original_error = getattr(error, "original", error)

        if isinstance(original_error, (commands.MissingAnyRole, commands.MissingRole)):
            await inter.response.send_message(
                "❌ You ain't got the right role for this command, chief.",
                ephemeral=True,
            )
        elif isinstance(original_error, commands.MemberNotFound):
            await inter.response.send_message(
                "❌ Can't find that user on this server. Make sure they're here and you spelled their name or ID right.",
                ephemeral=True,
            )
        elif isinstance(original_error, commands.UserNotFound):
            await inter.response.send_message(
                f"❌ No user with the ID `{original_error.argument}` found in Discord. Double-check that ID.",
                ephemeral=True,
            )
        elif isinstance(original_error, commands.CommandOnCooldown):
            await inter.response.send_message(
                f"⏳ Woah, slow down! This command is on cooldown. Try again in {original_error.retry_after:.2f} seconds.",
                ephemeral=True,
            )
        else:
            print(
                f"Ignoring exception in command {inter.application_command.name}",
                file=sys.stderr,
            )
            traceback.print_exception(
                type(original_error),
                original_error,
                original_error.__traceback__,
                file=sys.stderr,
            )
            if not inter.response.is_done():
                await inter.response.send_message(
                    "Something went sideways while running that command.",
                    ephemeral=True,
                )

    @commands.slash_command(name="mute", description="Timeout a user.")
    @commands.has_any_role(*MODERATOR_ROLE_IDS)
    async def mute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        time: str,
        reason: str,
        proof: str,
    ):
        try:
            duration = parse_duration(time)
        except ValueError as e:
            await inter.response.send_message(str(e), ephemeral=True)
            return

        if member.id == inter.author.id:
            await inter.response.send_message(
                "You can't mute yourself, silly.", ephemeral=True
            )
            return
        if member.id == self.bot.user.id:
            await inter.response.send_message(
                "You can't mute me, I'm untouchable.", ephemeral=True
            )
            return

        if member.top_role >= inter.guild.me.top_role:
            await inter.response.send_message(
                "I can't mute this user, their role is higher or equal to mine.",
                ephemeral=True,
            )
            return

        try:
            await member.timeout(duration=duration, reason=reason)
            await inter.response.send_message(
                f"Successfully timed out {member.mention} for `{time}`. Reason: {reason}",
                ephemeral=True,
            )
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                log_message = (
                    f"{inter.author.mention} (`{inter.author.id}`) timed out {member.mention} (`{member.id}`)"
                    f" for **{time}**. Reason: **{reason}**\n"
                    f"- **Proof:** {proof}"
                )
                await log_channel.send(log_message)
        except disnake.Forbidden:
            await inter.response.send_message(
                "I don't have permission to time out this user.",
                ephemeral=True,
            )
        except Exception as e:
            await inter.response.send_message(
                f"An unexpected error occurred: {e}", ephemeral=True
            )

    @commands.slash_command(name="unmute", description="Remove a user's timeout.")
    @commands.has_any_role(*MODERATOR_ROLE_IDS)
    async def unmute(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        reason: str,
    ):
        if not member.current_timeout:
            await inter.response.send_message(
                f"{member.mention} doesn't have an active timeout.", ephemeral=True
            )
            return
        if member.id == inter.author.id:
            await inter.response.send_message(
                "You can't remove a timeout from yourself.", ephemeral=True
            )
            return
        try:
            await member.timeout(duration=None, reason=reason)
            await inter.response.send_message(
                f"Successfully removed timeout from {member.mention}. Reason: {reason}",
                ephemeral=True,
            )
            log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
            if log_channel:
                await log_channel.send(
                    f"{inter.author.mention} (`{inter.author.id}`) removed timeout from {member.mention} (`{member.id}`) "
                    f". Reason: **{reason}**"
                )
        except disnake.Forbidden:
            await inter.response.send_message(
                "I don't have permission to remove timeouts from this user.",
                ephemeral=True,
            )
        except Exception as e:
            await inter.response.send_message(
                f"An unexpected error occurred: {e}", ephemeral=True
            )

    @commands.slash_command(
        name="form-ban",
        description="Request a ban for a user via an approval form.",
    )
    @commands.has_any_role(*MODERATOR_ROLE_IDS)
    async def form_ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        reason: str,
        proof: str,
    ):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            await inter.response.send_message(
                "Log channel not found. Contact an admin.",
                ephemeral=True,
            )
            return
        if member.id == inter.author.id:
            await inter.response.send_message(
                "You can't request a ban for yourself.", ephemeral=True
            )
            return
        if member.id == self.bot.user.id:
            await inter.response.send_message(
                "You can't request a ban for me.", ephemeral=True
            )
            return
        message_content = (
            f"<@&1398641721386078228>\n"
            f"{inter.author.mention} (`{inter.author.id}`) is requesting a ban for {member.mention} (`{member.id}`). Reason: **{reason}**.\n"
            f"- **Proof:** {proof}"
        )
        await log_channel.send(content=message_content, view=BanRequestView())
        await inter.response.send_message(
            "Your ban request has been sent for review.", ephemeral=True
        )

    @commands.slash_command(name="ban", description="Ban a user.")
    @commands.has_any_role(*APPROVER_ROLE_IDS)
    async def ban(
        self,
        inter: disnake.ApplicationCommandInteraction,
        user: disnake.User,
        reason: str,
    ):
        log_channel = self.bot.get_channel(LOG_CHANNEL_ID)
        if not log_channel:
            await inter.response.send_message(
                "Log channel not found. Contact an admin.",
                ephemeral=True,
            )
            return
        if user.id == inter.author.id:
            await inter.response.send_message(
                "You can't ban yourself.", ephemeral=True
            )
            return
        if user.id == self.bot.user.id:
            await inter.response.send_message(
                "You can't ban me.", ephemeral=True
            )
            return
        try:
            await inter.guild.ban(user, reason=f"Banned by {inter.author.name}: {reason}")
            await inter.response.send_message(
                f"User {user.mention} has been banned.", ephemeral=True
            )
            if log_channel:
                log_message = f"{inter.author.mention} (`{inter.author.id}`) banned user {user.mention} (`{user.id}`). Reason: **{reason}**"
                await log_channel.send(log_message)
        except disnake.Forbidden:
            await inter.response.send_message(
                "I don't have permission to ban this user.", ephemeral=True
            )
        except Exception as e:
            await inter.response.send_message(
                f"An unexpected error occurred: {e}", ephemeral=True
            )

    @commands.slash_command(
        name="moder-add", description="Make a user a moderator."
    )
    @commands.has_any_role(*APPROVER_ROLE_IDS)
    async def moder_add(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        reason: str,
    ):
        moder_role = inter.guild.get_role(MODERATOR_ROLE_ID)
        if not moder_role:
            await inter.response.send_message(
                "Moderator role not found on this server.", ephemeral=True
            )
            return
        if moder_role in member.roles:
            await inter.response.send_message(
                f"{member.mention} already has the moderator role.",
                ephemeral=True,
            )
            return
        await member.add_roles(
            moder_role, reason=f"Appointed by {inter.author.name}: {reason}"
        )
        self._reset_reprimands(member.id)
        await inter.response.send_message(
            f"You have successfully made {member.mention} a moderator.", ephemeral=True
        )
        log_channel = self.bot.get_channel(STAFF_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"{inter.author.mention} appointed a new moderator {member.mention}. Reason: **{reason}**."
            )

    @commands.slash_command(
        name="moder-remove", description="Remove a user from the moderator position."
    )
    @commands.has_any_role(*APPROVER_ROLE_IDS)
    async def moder_remove(
        self,
        inter: disnake.ApplicationCommandInteraction,
        member: disnake.Member,
        reason: str,
    ):
        moder_role = inter.guild.get_role(MODERATOR_ROLE_ID)
        if not moder_role:
            await inter.response.send_message(
                "Moderator role not found on this server.", ephemeral=True
            )
            return
        if moder_role not in member.roles:
            await inter.response.send_message(
                f"User {member.mention} does not have the moderator role.", ephemeral=True
            )
            return
        await member.remove_roles(
            moder_role, reason=f"Removed by {inter.author.name}: {reason}"
        )
        self._reset_reprimands(member.id)
        await inter.response.send_message(
            f"You have successfully removed {member.mention} from the moderator position.", ephemeral=True
        )
        log_channel = self.bot.get_channel(STAFF_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"{inter.author.mention} removed moderator {member.mention}. Reason: **{reason}**."
            )

    @commands.slash_command(name="vig-add", description="Give a reprimand to a moderator.")
    @commands.has_any_role(*APPROVER_ROLE_IDS)
    async def vig_add(
        self,
        inter: disnake.ApplicationCommandInteraction,
        moderator: disnake.Member,
        reason: str,
    ):
        moder_role = inter.guild.get_role(MODERATOR_ROLE_ID)
        if not moder_role:
            await inter.response.send_message(
                "Moderator role not found on this server.", ephemeral=True
            )
            return

        target_approver_roles = {role.id for role in moderator.roles}.intersection(
            APPROVER_ROLE_IDS
        )
        if target_approver_roles:
            await inter.response.send_message(
                "You can't give a reprimand to a senior moderator.", ephemeral=True
            )
            return

        if moder_role not in moderator.roles:
            await inter.response.send_message(
                f"User {moderator.mention} is not a moderator.",
                ephemeral=True,
            )
            return
        if moderator.id == inter.author.id:
            await inter.response.send_message(
                "You can't give a reprimand to yourself.", ephemeral=True
            )
            return
        new_count = self._add_reprimand(moderator.id)
        await inter.response.send_message(
            f"You have successfully given a reprimand to moderator {moderator.mention}. They now have {new_count}/3.",
            ephemeral=True,
        )
        log_channel = self.bot.get_channel(STAFF_LOG_CHANNEL_ID)
        if not log_channel:
            return
        if new_count >= 3:
            await moderator.remove_roles(moder_role, reason="3/3 reprimands")
            self._reset_reprimands(moderator.id)
            await log_channel.send(
                f"{inter.author.mention} removed moderator {moderator.mention}. Reason: **3/3 reprimands**."
            )
        else:
            await log_channel.send(
                f"{inter.author.mention} gave a reprimand `({new_count}/3)` to moderator {moderator.mention}. Reason: **{reason}**."
            )

    @commands.slash_command(
        name="vig-remove", description="Remove a reprimand from a moderator."
    )
    @commands.has_any_role(*APPROVER_ROLE_IDS)
    async def vig_remove(
        self,
        inter: disnake.ApplicationCommandInteraction,
        moderator: disnake.Member,
        reason: str,
    ):
        moder_role = inter.guild.get_role(MODERATOR_ROLE_ID)
        if not moder_role:
            await inter.response.send_message(
                "Moderator role not found on this server.", ephemeral=True
            )
            return

        target_approver_roles = {role.id for role in moderator.roles}.intersection(
            APPROVER_ROLE_IDS
        )
        if target_approver_roles:
            await inter.response.send_message(
                "You can't remove a reprimand from a senior moderator.", ephemeral=True
            )
            return

        if moder_role not in moderator.roles:
            await inter.response.send_message(
                f"User {moderator.mention} is not a moderator.",
                ephemeral=True,
            )
            return
        current_count = self._get_reprimands(moderator.id)
        if current_count == 0:
            await inter.response.send_message(
                f"Moderator {moderator.mention} has no reprimands.", ephemeral=True
            )
            return
        new_count = self._remove_reprimand(moderator.id)
        await inter.response.send_message(
            f"You have successfully removed a reprimand from moderator {moderator.mention}. They now have {new_count}/3.",
            ephemeral=True,
        )
        log_channel = self.bot.get_channel(STAFF_LOG_CHANNEL_ID)
        if log_channel:
            await log_channel.send(
                f"{inter.author.mention} removed a reprimand `({new_count}/3)` from moderator {moderator.mention}. Reason: **{reason}**."
            )


def setup(bot):
    bot.add_cog(UnifiedModerationCog(bot))
    print("[INFO] Cog 'UnifiedModerationCog' loaded successfully.")
