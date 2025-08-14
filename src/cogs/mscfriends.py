import disnake
from disnake.ext import commands, tasks
import asyncio

GUILD_ID = 1191694936723161159
VERIFICATION_CHANNEL_ID = 1393530748061094018
VERIFICATION_MESSAGE_ID = (
    1393562062030114816
)
VERIFIED_ROLE_ID = 1247453282507685932
REQUIRED_STATUS_TEXT = "discord.gg/pon"
REQUIRED_NICKNAME_TEXT = "ᵐˢᶜ"

EMBED_COLOR = disnake.Color(3092790)
IMAGE_URL_TOP = "https://media.discordapp.net/attachments/1307113271484219453/1399433592123166952/Frame_23.png?ex=6888fb98&is=6887aa18&hm=5874f1cd5670ce69725866162eb9ee6d5472d9951c993330dcd4d17c055a6b39&=&format=webp&quality=lossless"
IMAGE_URL_SEPARATOR = "https://cdn.discordapp.com/attachments/1307113271484219453/1324867860492976178/inv.png?ex=686461d8&is=68631058&hm=ac23c0a415450289e15f35ae23607738abf7de1926af94f0a0f5d17df45339d7&"


class MscFriendsCog(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.recheck_roles_task.start()

    def cog_unload(self):
        self.recheck_roles_task.cancel()

    @commands.Cog.listener()
    async def on_ready(self):
        self.bot.loop.create_task(self.setup_verification_message())
        print("[INFO] MscFriendsCog: Initial message setup task created.")

    async def setup_verification_message(self):
        await self.bot.wait_until_ready()
        try:
            channel = self.bot.get_channel(VERIFICATION_CHANNEL_ID)
            if not channel:
                print(
                    f"[ERROR] MscFriendsCog: Channel with ID {VERIFICATION_CHANNEL_ID} not found."
                )
                return

            message = await channel.fetch_message(VERIFICATION_MESSAGE_ID)
            if not message:
                print(
                    f"[ERROR] MscFriendsCog: Message with ID {VERIFICATION_MESSAGE_ID} not found."
                )
                return

            if message.author.id != self.bot.user.id:
                print(
                    f"[ERROR] MscFriendsCog: Cannot edit message {VERIFICATION_MESSAGE_ID} because it was not sent by the bot."
                )
                return

            embed_banner = disnake.Embed(color=EMBED_COLOR).set_image(url=IMAGE_URL_TOP)
            embed_main = disnake.Embed(
                description=(
                    "> <a:systemsolid50file:1270367630322044959>｜**Language selection:**\n\n" \
                    "```Click on the button with your language\'s flag.```\n\n"
                ),
                color=EMBED_COLOR,
            ).set_image(url=IMAGE_URL_SEPARATOR)

            view = disnake.ui.View(timeout=None)
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.secondary,
                    emoji="<:freeiconrussia197408:1236761146774654998>",
                    custom_id="msc_lang_russian",
                )
            )
            view.add_item(
                disnake.ui.Button(
                    style=disnake.ButtonStyle.secondary,
                    emoji="<:freeiconunitedkingdom8363075:1236761149018472469>",
                    custom_id="msc_lang_english",
                )
            )

            await message.edit(
                content=None, embeds=[embed_banner, embed_main], view=view
            )
            print(
                f"[INFO] MscFriendsCog: Message {VERIFICATION_MESSAGE_ID} has been successfully set up."
            )

        except Exception as e:
            print(
                f"[ERROR] MscFriendsCog: An unexpected error occurred during message setup: {e}"
            )

    @commands.Cog.listener()
    async def on_button_click(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id
        if not custom_id.startswith("msc_"):
            return

        if not inter.guild:
            return

        if custom_id in ["msc_lang_russian", "msc_lang_english"]:

            title = "MSC Friends"
            desc_line1 = "To get the role, you gotta do one of these things:"
            desc_line2 = f"Add `{REQUIRED_STATUS_TEXT}` to your status."
            desc_line3 = f"Add `{REQUIRED_NICKNAME_TEXT}` to your display name."
            button_label = "Check"

            embed_banner = disnake.Embed(color=EMBED_COLOR).set_image(url=IMAGE_URL_TOP)
            embed_main = disnake.Embed(
                title=f"<a:systemsolid42search:1315791752124432474>｜{title}",
                description=f"> {desc_line1}\n\n" + \
                            f"- {desc_line2}\n" + \
                            f"- {desc_line3}\n\n" + \
                            "```{desc_line4}```",
                color=EMBED_COLOR,
            ).set_image(url=IMAGE_URL_SEPARATOR)

            view = disnake.ui.View()
            view.add_item(
                disnake.ui.Button(
                    label=button_label,
                    style=disnake.ButtonStyle.secondary,
                    custom_id="msc_start_verification_{lang_suffix}",
                )
            )

            await inter.response.send_message(
                embeds=[embed_banner, embed_main], view=view, ephemeral=True
            )

        elif custom_id.startswith("msc_start_verification_"):
            await inter.response.defer(ephemeral=True)
            member = inter.author
            role = inter.guild.get_role(VERIFIED_ROLE_ID)

            if role and role in member.roles:
                msg = "You already got the role, fam."
                await inter.followup.send(f"❌ {msg}", ephemeral=True)
                return

            is_verified, reason = await self._perform_verification(member)

            if not role:
                await inter.followup.send(
                    "Error: Role to be assigned not found on the server.", ephemeral=True
                )
                print(
                    f"[ERROR] MscFriendsCog: Role with ID {VERIFIED_ROLE_ID} not found."
                )
                return

            if is_verified:
                await member.add_roles(role, reason=f"Passed verification ({reason})")
                success_msg = "You passed the vibe check."
                await inter.followup.send(
                    f"✅ {success_msg} ({reason})", ephemeral=True
                )
            else:
                fail_msg = "> ❌ **Verification failed. Make sure you\'ve done at least one of these:**\n\n" + \
                           f"- Text `{REQUIRED_STATUS_TEXT}` in your custom status.\n" + \
                           f"- Symbols `{REQUIRED_NICKNAME_TEXT}` in your display name."

                await inter.followup.send(fail_msg, ephemeral=True)

    async def _perform_verification(self, member: disnake.Member) -> tuple[bool, str]:
        """Checks if the user meets one of the two criteria. Returns (Passed?, Reason)"""
        try:
            fresh_member = await member.guild.fetch_member(member.id)
        except Exception as e:
            print(
                f"[ERROR] MscFriendsCog: Could not get fresh data for {member.id}: {e}"
            )
            return False, "API error"

        if fresh_member.activity and isinstance(
            fresh_member.activity, disnake.CustomActivity
        ):
            if (
                fresh_member.activity.name
                and REQUIRED_STATUS_TEXT in fresh_member.activity.name
            ):
                return True, "status check"

        if (
            fresh_member.global_name
            and REQUIRED_NICKNAME_TEXT in fresh_member.global_name
        ):
            return True, "global name check"

        return False, "conditions not met"

    @tasks.loop(hours=1)
    async def recheck_roles_task(self):
        await self.bot.wait_until_ready()
        print("[INFO] MscFriendsCog: Starting periodic role check...")
        guild = self.bot.get_guild(GUILD_ID)
        if not guild:
            print(f"[ERROR] MscFriendsCog Task: Server with ID {GUILD_ID} not found.")
            return

        role = guild.get_role(VERIFIED_ROLE_ID)
        if not role:
            print(
                f"[ERROR] MscFriendsCog Task: Role with ID {VERIFIED_ROLE_ID} not found."
            )
            return

        members_with_role = list(role.members)
        print(
            f"[INFO] MscFriendsCog Task: Found {len(members_with_role)} members with the role to check."
        )

        for member in members_with_role:
            try:
                is_still_verified, _ = await self._perform_verification(member)
                if not is_still_verified:
                    await member.remove_roles(role, reason="Re-check failed")
                    print(
                        f"[INFO] MscFriendsCog Task: Removed role from {member.display_name} ({member.id}) because they no longer meet the conditions."
                    )
                await asyncio.sleep(2)
            except Exception as e:
                print(
                    f"[ERROR] MscFriendsCog Task: Error checking member {member.id}: {e}"
                )

        print("[INFO] MscFriendsCog: Periodic role check finished.")


def setup(bot):
    bot.add_cog(MscFriendsCog(bot))
    print("[INFO] Cog 'MscFriendsCog' loaded successfully.")
