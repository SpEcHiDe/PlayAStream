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


from typing import Tuple
from pyrogram import filters
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from bot import (
    GROUP_CALLS,
    AUTH_USERS,
    LOGGER,
    COMMAND_HANDLER,
    PLAY_COMMAND_HNTTH,
    START_ED_PROC_ING_MESG,
    END_ED_PROC_ING_MESG
)
from bot.bot import Bot
from bot.helpers.yt_direct_link_genr import get_stream_url


@Bot.on_message(
    filters.user(AUTH_USERS) &
    filters.command(PLAY_COMMAND_HNTTH, COMMAND_HANDLER)
)
async def play_cmnd_fn(_, message: Message):
    # send a message, use it to update the progress when required
    status_message = await message.reply_text(
        START_ED_PROC_ING_MESG,
        quote=True
    )

    if not message.reply_to_message:
        await status_message.delete()
        return

    try:
        _chat_id = message.command[1]
        if _chat_id.startswith("-100"):
            _chat_id = int(_chat_id)
        else:
            _chat_id = (
                await message._client.get_chat(
                    _chat_id
                )
            ).id
    except IndexError:
        _chat_id = message.chat.id

    try:
        join_as = message.command[2]
        if join_as.startswith("-100"):
            join_as = int(join_as)
        else:
            join_as = (
                await message._client.get_chat(
                    join_as
                )
            ).id
    except IndexError:
        join_as = None

    stream_url = None
    try:
        stream_url = await get_stream_url(
            message.reply_to_message
        )
    except (AttributeError, IndexError):
        LOGGER(__name__).exception("stream link error")
    LOGGER(__name__).info(stream_url)

    if not stream_url:
        stream_url = message.reply_to_message.text

    group_call = GROUP_CALLS.get(_chat_id)
    if group_call is None:
        group_call = GroupCallFactory(
            message._client,
            enable_logs_to_console=False,
            path_to_log_file=None,
            outgoing_audio_bitrate_kbit=512
        ).get_group_call(
        )
        GROUP_CALLS[_chat_id] = group_call

    await group_call.join(
        _chat_id,
        join_as=join_as,
        enable_action=False
    )
    video_url, audio_url = (None, None)
    if isinstance(stream_url, Tuple):
        video_url, audio_url = stream_url
    else:
        video_url = stream_url
        audio_url = stream_url

    if video_url == audio_url:
        await group_call.start_video(
            video_url,
            with_audio=True,
            repeat=False
        )
    else:
        await group_call.start_audio(
            audio_url,
            repeat=False
        )
        await group_call.start_video(
            video_url,
            with_audio=False,
            repeat=False
        )

    await status_message.edit_text(END_ED_PROC_ING_MESG)
