#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  GetSongsBot
#  Copyright (C) 2021 The Authors

#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Affero General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.

#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Affero General Public License for more details.

#  You should have received a copy of the GNU Affero General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


from typing import Tuple
from pyrogram.types import Message
from bot import (
    LOGGER,
    TG_DUMP_CHAT,
    TG_M_STREAM_URL,
    YOUTUBE_DL_CMND
)
from .run_shell_command import run_command
from .link_fliter import extract_link


async def get_ytdl_link(original_yt_link: str) -> Tuple[str, str]:
    """ get the video link of a yt_dl html link
    """
    process = await run_command([
        YOUTUBE_DL_CMND,
        "-g",
        original_yt_link
    ])
    stdout, _ = await process.communicate()
    stdout = stdout.decode().strip()
    LOGGER(__name__).info(stdout)
    links = stdout.split("\n")
    return (links[0], links[-1])


async def get_stream_url(incoming_message: Message) -> str:
    """ get the video link from a tg message
    """
    stream_url = None

    if incoming_message and incoming_message.audio:
        fwded_mesg = await incoming_message.forward(
            TG_DUMP_CHAT
        )
        stream_url = f"{TG_M_STREAM_URL}/{fwded_mesg.message_id}/media"

    elif incoming_message:
        original_url, _ = extract_link(incoming_message)
        if original_url and "youtu" in original_url:
            stream_url = await get_ytdl_link(original_url)
        elif original_url:
            stream_url = original_url

    return stream_url
