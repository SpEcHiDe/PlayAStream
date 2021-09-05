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


def extract_link(message: Message) -> Tuple[str, str]:
    leech_url = None
    custom_file_name = None
    entities = (
        message.entities or
        message.caption_entities or
        []
    )
    text = (
        message.text or
        message.caption or
        ""
    )
    if message and text and len(entities) > 0:
        for one_entity in entities:
            if one_entity.type == "url":
                leech_url = text[
                    one_entity.offset:one_entity.offset + one_entity.length
                ]
            elif one_entity.type == "text_link":
                leech_url = one_entity.url
            if leech_url:
                break
        if "|" in text:
            _, custom_file_name = text.split("|", maxsplit=1)
        if leech_url:
            leech_url = leech_url.strip()
        if custom_file_name:
            custom_file_name = custom_file_name.strip()
        else:
            custom_file_name = None
    return (leech_url, custom_file_name)
