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


import json
from asyncio import sleep
from typing import Tuple
from pyrogram import filters
from pyrogram.errors import ChatAdminRequired
from pyrogram.raw.functions.channels import GetFullChannel
from pyrogram.raw.functions.phone import EditGroupCallTitle
from pyrogram.raw.functions.phone import ToggleGroupCallRecord
from pyrogram.types import Message
from pytgcalls import GroupCallFactory
from bot import (
    GROUP_CALLS,
    AUTH_USERS,
    LOGGER,
    STREAM_STATION_ID,
    TG_DUMP_CHAT,
    COMMAND_HANDLER,
    START_ED_PROC_ING_MESG,
    TG_RADIO_START_COMMAND_HTTNH,
    TG_RADIO_STOP_COMMAND_HTTNH
)
from bot.bot import Bot
from bot.helpers.yt_direct_link_genr import get_ytdl_link


@Bot.on_message(
    filters.user(AUTH_USERS) &
    filters.command(
        TG_RADIO_START_COMMAND_HTTNH,
        COMMAND_HANDLER
    )
)
async def hc_stream_radio_(client: Bot, message: Message):
    # send a message, use it to update the progress when required
    status_message = await message.reply_text(
        START_ED_PROC_ING_MESG,
        quote=True
    )

    dump_message_ = await client.get_messages(
        chat_id=TG_DUMP_CHAT,
        message_ids=STREAM_STATION_ID,
        replies=0
    )
    dump_message_text = (
        dump_message_.text or
        dump_message_.caption or
        "[]"
    )
    all_radio_stations = json.loads(dump_message_text)

    for one_radio in all_radio_stations:
        _chat_id = one_radio.get("CHANNEL")
        join_as = one_radio.get("JOINAS")
        stream_url = one_radio.get("URL")
        group_call_title = one_radio.get("TITLE", "@GetSongs")

        if _chat_id.startswith("-100"):
            _chat_id = int(_chat_id)

        _chat_id = (
            await message._client.get_chat(
                _chat_id
            )
        ).id

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

        if "youtu.be" in stream_url:
            stream_url = await get_ytdl_link(stream_url)

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

        try:
            peer = await message._client.resolve_peer(_chat_id)
            chat = await message._client.send(
                GetFullChannel(
                    channel=peer
                )
            )
            await message._client.send(
                EditGroupCallTitle(
                    call=chat.full_chat.call,
                    title=group_call_title
                )
            )
            await client.send(
                ToggleGroupCallRecord(
                    call=chat.full_chat.call,
                    start=True,
                    title=group_call_title
                )
            )
        except ChatAdminRequired:
            LOGGER(__name__).exception(msg="edit title error")
        await sleep(3)

    await status_message.delete()


@Bot.on_message(
    filters.user(AUTH_USERS) &
    filters.command(
        TG_RADIO_STOP_COMMAND_HTTNH,
        COMMAND_HANDLER
    )
)
async def hc_stream_radio_stop(client: Bot, message: Message):
    # send a message, use it to update the progress when required
    status_message = await message.reply_text(
        START_ED_PROC_ING_MESG,
        quote=True
    )

    dump_message_ = await client.get_messages(
        chat_id=TG_DUMP_CHAT,
        message_ids=STREAM_STATION_ID,
        replies=0
    )
    dump_message_text = (
        dump_message_.text or
        dump_message_.caption or
        "[]"
    )
    all_radio_stations = json.loads(dump_message_text)

    for one_radio in all_radio_stations:
        _chat_id = one_radio.get("CHANNEL")
        group_call_title = one_radio.get("TITLE", "@PlayAStream")

        if _chat_id.startswith("-100"):
            _chat_id = int(_chat_id)

        _chat_id = (
            await message._client.get_chat(
                _chat_id
            )
        ).id

        try:
            peer = await message._client.resolve_peer(_chat_id)
            chat = await message._client.send(
                GetFullChannel(
                    channel=peer
                )
            )
            await client.send(
                ToggleGroupCallRecord(
                    call=chat.full_chat.call,
                    start=False,
                    title=group_call_title
                )
            )
        except ChatAdminRequired:
            LOGGER(__name__).exception(msg="invalid admin error")

        group_call = GROUP_CALLS.get(_chat_id)
        if group_call:
            await group_call.stop()

    await status_message.delete()
