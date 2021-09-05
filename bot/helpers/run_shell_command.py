#!/usr/bin/env python3
#  -*- coding: utf-8 -*-
#  Copyright (C) 2020 PublicLeech Authors

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

import asyncio
from asyncio.subprocess import Process
from typing import List


async def run_command(shell_command: List) -> Process:
    """ executes a shell_command,
    and returns the stdout and stderr"""
    process = await asyncio.create_subprocess_exec(
        *shell_command,
        # stdout must a pipe to be accessible as process.stdout
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE,
    )
    return process
