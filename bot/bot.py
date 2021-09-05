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

""" MtProto Bot """

import os
import shutil
from pyrogram import (
    Client,
    __version__
)
from bot import (
    API_HASH,
    APP_ID,
    LOGGER,
    TEMP_DOWNLOAD_DIRS,
    TG_BOT_SESSION,
    TG_BOT_WORKERS
)


class Bot(Client):
    """ modded client """

    def __init__(self):
        super().__init__(
            TG_BOT_SESSION,
            api_hash=API_HASH,
            api_id=APP_ID,
            plugins={
                "root": "bot/plugins"
            },
            workers=TG_BOT_WORKERS,
            parse_mode="html",
            sleep_threshold=300,
            workdir=TEMP_DOWNLOAD_DIRS
        )
        self.LOGGER = LOGGER

    async def start(self):
        if not os.path.exists(TEMP_DOWNLOAD_DIRS):
            os.makedirs(TEMP_DOWNLOAD_DIRS)

        await super().start()
        usr_bot_me = await self.get_me()

        self.LOGGER(__name__).info(
            f"@{usr_bot_me.username} based-on "
            f"Pyrogram v{__version__} started. "
            "join @GetSongs"
        )

    async def stop(self, *args):
        await super().stop()
        shutil.rmtree(
            TEMP_DOWNLOAD_DIRS,
            ignore_errors=True
        )
        self.LOGGER(__name__).info("@GetSongs stopped. Bye.")
