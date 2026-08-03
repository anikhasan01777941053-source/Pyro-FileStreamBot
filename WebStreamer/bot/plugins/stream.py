# (c) @EverythingSuckz | @AbirHasan2005

import asyncio
import aiohttp
import urllib.parse
import os

from WebStreamer.bot import StreamBot
from WebStreamer.utils.database import Database
from WebStreamer.utils.human_readable import humanbytes
from WebStreamer.vars import Var

from pyrogram import filters, Client
from pyrogram.errors import FloodWait, UserNotParticipant
from pyrogram.types import (
    Message,
    InlineKeyboardMarkup,
    InlineKeyboardButton,
)

db = Database(
    Var.DATABASE_URL,
    Var.SESSION_NAME
)

SERVER_URL = os.getenv(
    "SERVER_URL",
    "https://videoprocessingserver-rj5a.onrender.com"
).rstrip("/")

BASE_URL = os.getenv(
    "BASE_URL",
    ""
).rstrip("/")


def get_media_file_size(m):
    media = m.video or m.audio or m.document

    if media and media.file_size:
        return media.file_size

    return None


def get_media_file_name(m):
    media = m.video or m.document or m.audio

    if media and media.file_name:
        return urllib.parse.quote_plus(media.file_name)

    return None
    
@StreamBot.on_message(
    filters.private
    & (filters.document | filters.video | filters.audio)
    & ~filters.edited,
    group=4
)
async def private_receive_handler(c: Client, m: Message):

    try:

        if not await db.is_user_exist(m.from_user.id):

            await db.add_user(m.from_user.id)

            await c.send_message(
                Var.BIN_CHANNEL,
                f"#NEW_USER:\n\nNew User [{m.from_user.first_name}](tg://user?id={m.from_user.id}) Started !!"
            )

        log_msg = await m.forward(chat_id=Var.BIN_CHANNEL)

        file_name = get_media_file_name(m)

        if not file_name:
            file_name = str(log_msg.message_id)

        file_size = humanbytes(get_media_file_size(m))

        stream_link = (
            f"{BASE_URL}/"
            f"{log_msg.message_id}/"
            f"{file_name}"
        )

        process_api = (
            f"{SERVER_URL}/api/process"
            f"?stream_url={urllib.parse.quote(stream_link, safe='')}"
            f"&title={urllib.parse.quote(file_name, safe='')}"
        )

        processing_msg = await m.reply_text(
            "⏳ Processing Video...\nPlease wait..."
        )

        async with aiohttp.ClientSession() as session:

            async with session.get(process_api) as resp:
                process_data = await resp.json()

            if not process_data.get("success"):

                await processing_msg.edit_text(
                    f"❌ {process_data.get('error', 'Unknown Error')}"
                )

                return

            status_url = (
                f"{SERVER_URL}/api/status"
                f"?title={urllib.parse.quote(file_name, safe='')}"
            )

            while True:

                await asyncio.sleep(5)

                async with session.get(status_url) as check:
                    status = await check.json()

                if status.get("status") == "completed":

                    links = status.get("download_links", {})

                    text = (
                        "✅ Processing Completed!\n\n"
                        "🎬 HLS Stream\n"
                        f"{status['hls_stream_link']}\n\n"
                        "📥 720p Download\n"
                        f"{links.get('720p', 'Not Available')}"
                    )

                    await processing_msg.edit_text(
                        text,
                        disable_web_page_preview=True
                    )

                    break

                elif status.get("status") == "failed":

                    await processing_msg.edit_text(
                        "❌ Video Processing Failed."
                    )

                    break

    except FloodWait as e:

        print(f"Sleeping for {e.x} seconds")

        await asyncio.sleep(e.x)

    except Exception as e:

        print(e)

        await m.reply_text(
            f"❌ Error:\n`{e}`"
        )
                
@StreamBot.on_message(
    filters.channel
    & (filters.document | filters.video)
    & ~filters.edited,
    group=-1
)
async def channel_receive_handler(bot, broadcast):

    if int(broadcast.chat.id) in Var.BANNED_CHANNELS:
        await bot.leave_chat(broadcast.chat.id)
        return

    try:

        log_msg = await broadcast.forward(
            chat_id=Var.BIN_CHANNEL
        )

        await log_msg.reply_text(
            text=(
                f"**Channel Name:** `{broadcast.chat.title}`\n"
                f"**Channel ID:** `{broadcast.chat.id}`\n"
                f"**Link:** "
                f"https://t.me/{(await bot.get_me()).username}"
                f"?start=AbirHasan2005_{log_msg.message_id}"
            ),
            quote=True,
            parse_mode="Markdown"
        )

        await bot.edit_message_reply_markup(
            chat_id=broadcast.chat.id,
            message_id=broadcast.message_id,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "Get Direct Download Link",
                            url=(
                                f"https://t.me/{(await bot.get_me()).username}"
                                f"?start=AbirHasan2005_{log_msg.message_id}"
                            )
                        )
                    ]
                ]
            )
        )

    except FloodWait as e:

        print(f"Sleeping for {e.x} seconds")

        await asyncio.sleep(e.x)

        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=(
                f"Got FloodWait of {e.x}s\n\n"
                f"Channel ID: `{broadcast.chat.id}`"
            ),
            parse_mode="Markdown"
        )

    except Exception as e:

        print(e)

        await bot.send_message(
            chat_id=Var.BIN_CHANNEL,
            text=f"#ERROR\n`{e}`",
            parse_mode="Markdown"
        )               