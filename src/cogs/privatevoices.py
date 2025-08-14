import disnake
from disnake.ext import commands

GUILD_ID = 1191694936723161159
CREATOR_CHANNEL_ID = 1390984816727425074
CATEGORY_ID = 1390984700415316071
PANEL_CHANNEL_ID = 1390984783009415209
PANEL_MESSAGE_ID = 1390986859173249075
COMMUNITY_ROLE_IDS = [1399463626263232522, 1399463633674833920]

IMAGE_URL_TOP = "https://media.discordapp.net/attachments/1307113271484219453/1399433592123166952/Frame_23.png?ex=6888fb98&is=6887aa18&hm=5874f1cd5670ce69725866162eb9ee6d5472d9951c993330dcd4d17c055a6b39&=&format=webp&quality=lossless"
IMAGE_URL_BOTTOM = "https://cdn.discordapp.com/attachments/1307113271484219453/1324867860492976178/inv.png?ex=686461d8&is=68631058&hm=ac23c0a415450289e15f35ae23607738abf7de1926af94f0a0f5d17df45339d7&"

PANEL_TEXTS = {
    "ru": {
        "description": (
            "> <a:systemsolid22build:1270390000147501138>｜**Панель управления приватной комнатой:**\n\n"
            "- **👥 Лимит:** Установить максимальное количество участников.\n"
            "- **🚫 Кикнуть:** Выгнать пользователя из вашей комнаты.\n"
            "- **👁️ Скрыть/Показать:** Сделать комнату невидимой/видимой для всех.\n"
            "- **🔒 Закрыть/Открыть:** Запретить/разрешить всем заходить в комнату.\n"
            "- **🔑 Доступ:** Разрешить/запретить/сбросить права для конкретного пользователя."
        )
    },
    "en": {
        "description": (
            "> <a:systemsolid22build:1270390000147501138>｜**Your Crib's Control Panel:**\n\n"
            "- **👥 Limit:** Set how many peeps can join.\n"
            "- **🚫 Kick:** Boot someone from your room.\n"
            "- **👁️ Hide/Show:** Make your room go ghost or be seen by all.\n"
            "- **🔒 Lock/Unlock:** Lock it down or open it up for everyone.\n"
            "- **🔑 Access:** Give, deny, or reset perms for a specific user."
        )
    },
}

BUTTON_LABELS = {
    "ru": {
        "limit": "Лимит",
        "kick": "Кикнуть",
        "visibility": "Скрыть/Показать",
        "lock": "Закрыть/Открыть",
        "access": "Доступ",
    },
    "en": {
        "limit": "Limit",
        "kick": "Kick",
        "visibility": "Stealth",
        "lock": "Lockdown",
        "access": "Access",
    },
}

MODAL_TEXTS = {
    "ru": {
        "set_limit_title": "Установить лимит",
        "set_limit_label": "Новый лимит участников",
        "set_limit_placeholder": "Введите число от 0 до 99 (0 = без лимита)",
        "kick_user_title": "Кикнуть пользователя",
        "kick_user_placeholder": "Введите ID пользователя для кика",
        "user_id_label": "ID Пользователя",
        "grant_access_title": "Выдать доступ",
        "grant_access_placeholder": "Введите ID пользователя",
        "revoke_access_title": "Запретить доступ",
        "revoke_access_placeholder": "Введите ID пользователя",
        "reset_access_title": "Сбросить права",
        "reset_access_placeholder": "Введите ID пользователя",
    },
    "en": {
        "set_limit_title": "Set Peep Limit",
        "set_limit_label": "New Peep Limit",
        "set_limit_placeholder": "Gimme a number 0-99 (0 = no limit)",
        "kick_user_title": "Boot User",
        "kick_user_placeholder": "Drop the user ID to boot 'em",
        "user_id_label": "User ID",
        "grant_access_title": "Give Access",
        "grant_access_placeholder": "Drop the user ID",
        "revoke_access_title": "Deny Access",
        "revoke_access_placeholder": "Drop the user ID",
        "reset_access_title": "Reset Perms",
        "reset_access_placeholder": "Drop the user ID",
    },
}

RESPONSE_TEXTS = {
    "ru": {
        "no_room": "❌ У вас нет приватной комнаты.",
        "limit_success": "✅ Лимит участников для вашей комнаты установлен на **{}**.",
        "limit_no_limit": "без ограничений",
        "limit_error": "❌ Ошибка: Введите корректное число от 0 до 99.",
        "visibility_hidden": "✅ Ваша комната теперь **скрыта**.",
        "visibility_visible": "✅ Ваша комната теперь **видна всем**.",
        "lock_closed": "✅ Ваша комната теперь **закрыта**.",
        "lock_open": "✅ Ваша комната теперь **открыта для всех**.",
        "invalid_id": "❌ Неверный ID или пользователь не найден на этом сервере.",
        "cant_manage_self": "❌ Вы не можете управлять доступом для самого себя.",
        "cant_kick_self": "❌ Вы не можете кикнуть самого себя.",
        "kick_success": "✅ Пользователь **{}** кикнут.",
        "kick_not_in_room": "❌ Пользователь не в вашей комнате.",
        "grant_success": "✅ Доступ для **{}** выдан.",
        "revoke_success": "✅ Доступ для **{}** запрещен.",
        "reset_success": "✅ Все особые права для **{}** сброшены.",
        "access_denied_dm": "Вы не можете войти в комнату **{}**, так как она закрыта владельцем.",
        "hidden_denied_dm": "Вы не можете находиться в комнате **{}**, так как она была скрыта владельцем.",
        "select_action": "Выберите действие для пользователя...",
        "access_grant": "Разрешить подключение",
        "access_revoke": "Запретить подключение",
        "access_reset": "Сбросить права пользователя",
    },
    "en": {
        "no_room": "❌ Bruh, you ain't got no private room.",
        "limit_success": "✅ Aight, your room's peep limit is now **{}**.",
        "limit_no_limit": "no holds barred",
        "limit_error": "❌ Yo, that ain't right. Gimme a number from 0 to 99.",
        "visibility_hidden": "✅ Your room's in stealth mode now. **Hidden**.",
        "visibility_visible": "✅ Your room's public now. **Visible to all**.",
        "lock_closed": "✅ Your room's on **lockdown**.",
        "lock_open": "✅ Your room's **open for all**.",
        "invalid_id": "❌ That ID is bogus or the user ain't here.",
        "cant_manage_self": "❌ Can't mess with your own access, my dude.",
        "cant_kick_self": "❌ You can't boot yourself, silly.",
        "kick_success": "✅ User **{}** got the boot.",
        "kick_not_in_room": "❌ That user ain't in your room.",
        "grant_success": "✅ **{}** can now roll in.",
        "revoke_success": "✅ **{}** can't get in no more.",
        "reset_success": "✅ All special perms for **{}** are wiped.",
        "access_denied_dm": "You can't get into **{}**, the owner locked it down.",
        "hidden_denied_dm": "You can't be in **{}**, the owner made it go ghost.",
        "select_action": "Whatcha wanna do with this user...?",
        "access_grant": "Let 'em in",
        "access_revoke": "Keep 'em out",
        "access_reset": "Wipe user perms",
    },
}


class SetLimitModal(disnake.ui.Modal):
    def __init__(self, channel: disnake.VoiceChannel, lang: str):
        self.channel = channel
        self.lang = lang
        texts = MODAL_TEXTS[lang]
        components = [
            disnake.ui.TextInput(
                label=texts["set_limit_label"],
                placeholder=texts["set_limit_placeholder"],
                custom_id="limit_input",
                min_length=1,
                max_length=2,
            ),
        ]
        super().__init__(
            title=texts["set_limit_title"],
            components=components,
            custom_id=f"set_limit_modal_{lang}",
        )

    async def callback(self, inter: disnake.ModalInteraction):
        limit_str = inter.text_values["limit_input"]
        texts = RESPONSE_TEXTS[self.lang]
        try:
            limit = int(limit_str)
            if not 0 <= limit <= 99:
                raise ValueError
            await self.channel.edit(user_limit=limit)
            limit_text = limit if limit > 0 else texts["limit_no_limit"]
            await inter.response.send_message(
                texts["limit_success"].format(limit_text), ephemeral=True
            )
        except (ValueError, disnake.HTTPException):
            await inter.response.send_message(texts["limit_error"], ephemeral=True)


class UserIDModal(disnake.ui.Modal):
    def __init__(self, title: str, custom_id: str, placeholder: str, lang: str):
        texts = MODAL_TEXTS[lang]
        components = [
            disnake.ui.TextInput(
                label=texts["user_id_label"],
                placeholder=placeholder,
                custom_id="user_id_input",
                min_length=17,
                max_length=20,
            ),
        ]
        super().__init__(title=title, components=components, custom_id=custom_id)


class AccessControlSelect(disnake.ui.StringSelect):
    def __init__(self, lang: str):
        self.lang = lang
        texts = RESPONSE_TEXTS[lang]
        options = [
            disnake.SelectOption(
                label=texts["access_grant"],
                value=f"access_grant_select_{lang}",
                emoji="✅",
            ),
            disnake.SelectOption(
                label=texts["access_revoke"],
                value=f"access_revoke_select_{lang}",
                emoji="🚫",
            ),
            disnake.SelectOption(
                label=texts["access_reset"],
                value=f"access_reset_select_{lang}",
                emoji="🔄",
            ),
        ]
        super().__init__(
            placeholder=texts["select_action"],
            options=options,
            custom_id="access_control_select",
        )

    async def callback(self, inter: disnake.MessageInteraction):
        selected_option = inter.values[0]
        action, lang = selected_option.rsplit("_", 1)

        modal_map = {
            "access_grant_select": (
                "grant_access_title",
                f"grant_user_modal_{lang}",
                "grant_access_placeholder",
            ),
            "access_revoke_select": (
                "revoke_access_title",
                f"revoke_user_modal_{lang}",
                "revoke_access_placeholder",
            ),
            "access_reset_select": (
                "reset_access_title",
                f"reset_user_modal_{lang}",
                "reset_access_placeholder",
            ),
        }

        title_key, modal_cid, placeholder_key = modal_map[action]
        modal_texts = MODAL_TEXTS[lang]

        await inter.response.send_modal(
            UserIDModal(
                title=modal_texts[title_key],
                custom_id=modal_cid,
                placeholder=modal_texts[placeholder_key],
                lang=lang,
            )
        )


class AccessControlView(disnake.ui.View):
    def __init__(self, lang: str):
        super().__init__(timeout=180)
        self.add_item(AccessControlSelect(lang))


class LanguageSelectionView(disnake.ui.View):
    def __init__(self):
        super().__init__(timeout=None)

    @disnake.ui.button(
        style=disnake.ButtonStyle.secondary,
        emoji="<:freeiconrussia197408:1236761146774654998>",
        custom_id="panel_lang_ru",
    )
    async def russian_button(
        self,
        button: disnake.ui.Button,
        inter: disnake.MessageInteraction,
    ):
        pass

    @disnake.ui.button(
        style=disnake.ButtonStyle.secondary,
        emoji="<:freeiconunitedkingdom8363075:1236761149018472469>",
        custom_id="panel_lang_en",
    )
    async def english_button(
        self,
        button: disnake.ui.Button,
        inter: disnake.MessageInteraction,
    ):
        pass


class ControlPanelView(disnake.ui.View):
    def __init__(self, lang: str):
        super().__init__(timeout=None)
        labels = BUTTON_LABELS[lang]

        self.add_item(
            disnake.ui.Button(
                label=labels["limit"],
                style=disnake.ButtonStyle.secondary,
                emoji="👥",
                custom_id=f"voice_limit_{lang}",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label=labels["kick"],
                style=disnake.ButtonStyle.secondary,
                emoji="🚫",
                custom_id=f"voice_kick_{lang}",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label=labels["visibility"],
                style=disnake.ButtonStyle.secondary,
                emoji="👁️",
                custom_id=f"voice_visibility_{lang}",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label=labels["lock"],
                style=disnake.ButtonStyle.secondary,
                emoji="🔒",
                custom_id=f"voice_lock_{lang}",
            )
        )
        self.add_item(
            disnake.ui.Button(
                label=labels["access"],
                style=disnake.ButtonStyle.secondary,
                emoji="🔑",
                custom_id=f"voice_access_control_{lang}",
            )
        )


class VoiceSystem(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.user_channels = {}
        self.view_added = False

    async def setup_panel(self):
        try:
            channel = await self.bot.fetch_channel(PANEL_CHANNEL_ID)
            message = await channel.fetch_message(PANEL_MESSAGE_ID)

            embed1 = disnake.Embed(color=disnake.Color(3092790))
            embed1.set_image(url=IMAGE_URL_TOP)

            embed2 = disnake.Embed(
                description="> <a:systemsolid50file:1270367630322044959>｜**Choose your lingo:**\n\n```Click the button for your language.```",
                color=disnake.Color(3092790),
            )
            embed2.set_image(url=IMAGE_URL_BOTTOM)

            await message.edit(
                content=None, embeds=[embed1, embed2], view=LanguageSelectionView()
            )
            print(
                "[INFO] VoiceSystem: Language selection panel set up/updated successfully."
            )
        except (disnake.NotFound, disnake.Forbidden, Exception) as e:
            print(
                f"[ERROR] VoiceSystem: Error setting up language selection panel: {e}"
            )

    @commands.Cog.listener()
    async def on_ready(self):
        if not self.view_added:
            self.bot.add_view(LanguageSelectionView())
            self.view_added = True
            print("[INFO] VoiceSystem Views have been registered.")
            await self.setup_panel()
        print("[INFO] VoiceSystem Cog is ready.")

    async def get_user_room(self, user_id: int) -> disnake.VoiceChannel | None:
        channel_id = self.user_channels.get(user_id)
        if not channel_id:
            return None
        try:
            channel = await self.bot.fetch_channel(channel_id)
            if isinstance(channel, disnake.VoiceChannel):
                return channel
        except (disnake.NotFound, disnake.Forbidden):
            pass
        if user_id in self.user_channels:
            del self.user_channels[user_id]
        return None

    @commands.Cog.listener()
    async def on_voice_state_update(
        self,
        member: disnake.Member,
        before: disnake.VoiceState,
        after: disnake.VoiceState,
    ):
        if member.bot:
            return

        if after.channel and after.channel.id == CREATOR_CHANNEL_ID:
            user_room = await self.get_user_room(member.id)
            if user_room:
                try:
                    await member.move_to(user_room)
                except disnake.HTTPException:
                    pass
            else:
                guild = member.guild
                category = guild.get_channel(CATEGORY_ID)
                if not category:
                    return

                overwrites = {
                    guild.default_role: disnake.PermissionOverwrite(
                        view_channel=False, connect=True
                    ),
                    member: disnake.PermissionOverwrite(
                        view_channel=True, connect=True
                    ),
                }

                for role_id in COMMUNITY_ROLE_IDS:
                    role = guild.get_role(role_id)
                    if role:
                        overwrites[role] = disnake.PermissionOverwrite(
                            view_channel=True
                        )

                try:
                    channel_name = f"⸝⸝🎤・{member.name}"
                    new_channel = await category.create_voice_channel(
                        name=channel_name, overwrites=overwrites
                    )
                    self.user_channels[member.id] = new_channel.id
                    await member.move_to(new_channel)
                except disnake.HTTPException:
                    pass

        if after.channel and after.channel.id in self.user_channels.values():
            room = after.channel
            owner_id = next(
                (uid for uid, cid in self.user_channels.items() if cid == room.id), None
            )

            if member.id == owner_id:
                return

            user_overwrites = room.overwrites_for(member)
            if user_overwrites.connect is True and user_overwrites.view_channel is True:
                return

            everyone_overwrites = room.overwrites_for(member.guild.default_role)
            if everyone_overwrites.connect is False:
                await member.move_to(None, reason="Attempt to enter a locked room")
                try:
                    await member.send(
                        RESPONSE_TEXTS.get("en", {})
                        .get("access_denied_dm", "You cannot enter this room.")
                        .format(room.name),
                        delete_after=15,
                    )
                except disnake.Forbidden:
                    pass
                return

            community_role_to_check = room.guild.get_role(COMMUNITY_ROLE_IDS[0])
            if community_role_to_check:
                community_overwrites = room.overwrites_for(community_role_to_check)
                if community_overwrites.view_channel is False:
                    await member.move_to(None, reason="Attempt to enter a hidden room")
                    try:
                        await member.send(
                            RESPONSE_TEXTS.get("en", {})
                            .get("hidden_denied_dm", "You cannot be in this room.")
                            .format(room.name),
                            delete_after=15,
                        )
                    except disnake.Forbidden:
                        pass
                    return

        if before.channel and before.channel.id in self.user_channels.values():
            if not any(not m.bot for m in before.channel.members):
                owner_id = next(
                    (
                        user_id
                        for user_id, channel_id in self.user_channels.items()
                        if channel_id == before.channel.id
                    ),
                    None,
                )
                try:
                    await before.channel.delete(reason="Room is empty")
                    if owner_id and owner_id in self.user_channels:
                        del self.user_channels[owner_id]
                except disnake.HTTPException:
                    pass

    @commands.Cog.listener("on_button_click")
    async def on_interaction_router(self, inter: disnake.MessageInteraction):
        custom_id = inter.component.custom_id

        if custom_id.startswith("panel_lang_"):
            lang_code = custom_id.split("_")[-1]

            embed1 = disnake.Embed(color=disnake.Color(3092790))
            embed1.set_image(url=IMAGE_URL_TOP)

            embed2 = disnake.Embed(
                description=PANEL_TEXTS[lang_code]["description"],
                color=disnake.Color(3092790),
            )
            embed2.set_image(url=IMAGE_URL_BOTTOM)

            await inter.response.send_message(
                embeds=[embed1, embed2],
                view=ControlPanelView(lang=lang_code),
                ephemeral=True,
            )

        elif custom_id.startswith("voice_"):
            action, lang = custom_id.rsplit("_", 1)
            texts = RESPONSE_TEXTS[lang]

            room = await self.get_user_room(inter.author.id)
            if not room:
                await inter.response.send_message(texts["no_room"], ephemeral=True)
                return

            if action == "voice_limit":
                await inter.response.send_modal(modal=SetLimitModal(room, lang))
            elif action == "voice_kick":
                modal_texts = MODAL_TEXTS[lang]
                await inter.response.send_modal(
                    UserIDModal(
                        modal_texts["kick_user_title"],
                        f"kick_user_modal_{lang}",
                        modal_texts["kick_user_placeholder"],
                        lang,
                    )
                )

            elif action == "voice_visibility":
                role_to_check = inter.guild.get_role(COMMUNITY_ROLE_IDS[0])
                current_visibility = True
                if role_to_check:
                    current_visibility = (
                        room.overwrites_for(role_to_check).view_channel is True
                    )

                new_visibility = not current_visibility

                for role_id in COMMUNITY_ROLE_IDS:
                    role = inter.guild.get_role(role_id)
                    if role:
                        await room.set_permissions(role, view_channel=new_visibility)

                msg = (
                    texts["visibility_hidden"]
                    if not new_visibility
                    else texts["visibility_visible"]
                )
                await inter.response.send_message(msg, ephemeral=True)

            elif action == "voice_lock":
                current_overwrite = room.overwrites_for(inter.guild.default_role)
                is_unlocked = current_overwrite.connect is not False

                new_connect_state = not is_unlocked

                await room.set_permissions(
                    inter.guild.default_role,
                    view_channel=False,
                    connect=new_connect_state,
                )

                msg = (
                    texts["lock_closed"]
                    if not new_connect_state
                    else texts["lock_open"]
                )
                await inter.response.send_message(msg, ephemeral=True)
            elif action == "voice_access_control":
                await inter.response.send_message(
                    view=AccessControlView(lang), ephemeral=True
                )

    @commands.Cog.listener("on_modal_submit")
    async def on_panel_modal_submit(self, inter: disnake.ModalInteraction):
        custom_id = inter.custom_id
        action, lang = custom_id.rsplit("_", 1)

        if action not in [
            "kick_user_modal",
            "grant_user_modal",
            "revoke_user_modal",
            "reset_user_modal",
        ]:
            return

        texts = RESPONSE_TEXTS[lang]
        room = await self.get_user_room(inter.author.id)
        if not room:
            await inter.response.send_message(texts["no_room"], ephemeral=True)
            return

        try:
            target_member = await inter.guild.fetch_member(
                int(inter.text_values["user_id_input"])
            )
        except (ValueError, TypeError, disnake.NotFound):
            return await inter.response.send_message(
                texts["invalid_id"], ephemeral=True
            )

        if action in ["grant_user_modal", "revoke_user_modal", "reset_user_modal"]:
            if target_member.id == inter.author.id:
                return await inter.response.send_message(
                    texts["cant_manage_self"], ephemeral=True
                )

        if action == "kick_user_modal":
            if target_member.id == inter.author.id:
                return await inter.response.send_message(
                    texts["cant_kick_self"], ephemeral=True
                )
            if target_member.voice and target_member.voice.channel == room:
                await target_member.move_to(None, reason="Kicked by room owner")
                await inter.response.send_message(
                    texts["kick_success"].format(target_member.display_name),
                    ephemeral=True,
                )
            else:
                await inter.response.send_message(
                    texts["kick_not_in_room"], ephemeral=True
                )

        elif action == "grant_user_modal":
            await room.set_permissions(target_member, connect=True, view_channel=True)
            await inter.response.send_message(
                texts["grant_success"].format(target_member.display_name),
                ephemeral=True,
            )
        elif action == "revoke_user_modal":
            await room.set_permissions(target_member, connect=False)
            await inter.response.send_message(
                texts["revoke_success"].format(target_member.display_name),
                ephemeral=True,
            )
        elif action == "reset_user_modal":
            await room.set_permissions(target_member, overwrite=None)
            await inter.response.send_message(
                texts["reset_success"].format(target_member.display_name),
                ephemeral=True,
            )


def setup(bot: commands.Bot):
    bot.add_cog(VoiceSystem(bot))
    print("[INFO] Cog 'Private Voices' loaded.")