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

""" credentials """

import logging
import os
from dotenv import load_dotenv
from logging.handlers import RotatingFileHandler
from bot.get_config import get_config


# apparently, no error appears even if the path does not exists
load_dotenv("config.env")


# The Telegram API things
# Get these values from my.telegram.org or Telegram: @useTGxBot
API_HASH = get_config("API_HASH", should_prompt=True)
APP_ID = int(get_config("APP_ID", should_prompt=True))
TG_BOT_SESSION = get_config("TG_BOT_SESSION", "bot")
# Number of update workers to use.
# 4 is the recommended (and default) amount,
# but your experience may vary.
# Note that going crazy with more workers
# wont necessarily speed up your bot,
# given the amount of sql data accesses,
# and the way python asynchronous calls work.
TG_BOT_WORKERS = int(get_config("TG_BOT_WORKERS", "4"))
# path to store LOG files
LOG_FILE_ZZGEVC = get_config("LOG_FILE_ZZGEVC", "GetSongs.log")
# download directory
TEMP_DOWNLOAD_DIRS = os.path.abspath(
    get_config(
        "TEMP_DOWNLOAD_DIRS",
        "./DLS/"
    )
)
# @pit_DBAAS :( hope it won't be a failure, this time?
STREAM_STATION_ID = int(get_config("STREAM_STATION_ID", "0"))
COMMAND_HANDLER = get_config("COMMAND_HANDLER", "/")
# memes
HELP_STICKER = "CAADAgAD6AkAAowucAABsFGHedLEzeUWBA"
STOP_SPAMMING_STICKER = "CAADAgAD9AkAAowucAABLcWjFAPIoUEWBA"
# files
TG_DUMP_CHAT = int(get_config(
    "TG_DUMP_CHAT",
    "-100"
))
AUTH_USERS = list(set(
    int(x) for x in get_config("AUTH_USERS").split(" ")
))
TG_M_STREAM_URL = get_config("TG_M_STREAM_URL")
YOUTUBE_DL_CMND = get_config("YOUTUBE_DL_CMND", "youtube-dl")

logging.basicConfig(
    level=logging.INFO,
    format="[%(asctime)s - %(levelname)s] - %(name)s - %(message)s",
    datefmt='%d-%b-%y %H:%M:%S',
    handlers=[
        RotatingFileHandler(
            LOG_FILE_ZZGEVC,
            maxBytes=50000000,
            backupCount=1
        ),
        logging.StreamHandler()
    ]
)
logging.getLogger("pyrogram").setLevel(logging.WARNING)


def LOGGER(name: str) -> logging.Logger:
    """ get a Logger object """
    return logging.getLogger(name)


# a dictionary to store the currently running processes
GROUP_CALLS = {}

# strings
UN_MUTE_COMMAND_HNTTH = get_config("UN_MUTE_COMMAND_HNTTH", "unmute")
MUTE_COMMAND_HNTTH = get_config("MUTE_COMMAND_HNTTH", "mute")
SHOULD_DIS_ALLOW_PMS = bool(get_config("SHOULD_DIS_ALLOW_PMS", False))
PLAY_COMMAND_HNTTH = get_config("PLAY_COMMAND_HNTTH", "play")
STOP_COMMAND_HNTTH = get_config("STOP_COMMAND_HNTTH", "stop")
START_ED_PROC_ING_MESG = get_config("START_ED_PROC_ING_MESG", "⚡️")
END_ED_PROC_ING_MESG = get_config("END_ED_PROC_ING_MESG", "😴")
TG_RADIO_START_COMMAND_HTTNH = get_config(
    "TG_RADIO_START_COMMAND_HTTNH",
    "radiostart"
)
TG_RADIO_STOP_COMMAND_HTTNH = get_config(
    "TG_RADIO_STOP_COMMAND_HTTNH",
    "radiostop"
)
