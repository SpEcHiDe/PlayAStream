#!/usr/bin/env python3
# -*- coding: utf-8 -*-
# Copyright (C) @GetSongs
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU Affero General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Affero General Public License for more details.

# You should have received a copy of the GNU Affero General Public License
# along with this program.  If not, see <https://www.gnu.org/licenses/>.


from pyrogram import filters
from pyrogram.types import Message
from bot import (
    AUTH_USERS,
    SHOULD_ALLOW_PMS
)
from bot.bot import Bot


def pm_filter(_, __, message: Message):
    return (
        SHOULD_ALLOW_PMS and
        message and
        message.from_user and
        not message.from_user.is_bot and
        not message.from_user.is_contact and
        not message.from_user.is_verified and
        not message.from_user.is_support and
        message.chat and
        message.chat.type == "private"
    )


@Bot.on_message(
    ~filters.user(AUTH_USERS) &
    filters.create(pm_filter)
)
async def on_other_users_messages(_, message: Message):
    await message.delete()
