from pyrogram.types import Message
from bot import TG_DUMP_CHAT, TG_M_STREAM_URL, LOGGER
from .run_shell_command import run_command
from .link_fliter import extract_link


async def get_ytdl_link(original_yt_link: str):
    process = await run_command([
        "youtube-dl",
        "-g",
        original_yt_link,
        # "-f",
        # "b[ext=mp4]"
    ])
    stdout, _ = await process.communicate()
    stdout = stdout.decode().strip()
    LOGGER(__name__).info(stdout)
    links = stdout.split("\n")
    return (links[0], links[-1])


async def get_stream_url(incoming_message: Message) -> str:
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
