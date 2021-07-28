"""
Vimeo downloader bot
Copyright (C) 2021 @ImJanindu

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program.  If not, see <https://www.gnu.org/licenses/>.
"""

# Kang with credits vomro

import os
import logging
from pyrogram import filters, Client, idle
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from vimeo_downloader import Vimeo
from sample_config import Config

# location
LOCATION = "./"

# logging
bot = Client(
   "Vimeo",
   api_id=Config.API_ID,
   api_hash=Config.API_HASH,
   bot_token=Config.BOT_TOKEN,
)

# start message
@bot.on_message(filters.command("start") & filters.private)
async def start(_, message):
   user = message.from_user.mention
   await message.reply_text(f"""Hey {user}, I'm Vimeo downloader bot ✨

I can download vimeo video links and upload to Telegram 💥
Send me a vimeo video link to start download 🚿""",
       reply_markup = InlineKeyboardMarkup([[InlineKeyboardButton("💻 Update Channel 💻", url="https://t.me/FZBOTS")]]))

# vimeo download
@bot.on_message(filters.regex(pattern="https://vimeo.com/") & filters.private)
async def vimeo(_, message):
    input = message.text
    user = message.from_user.mention
    msg = await message.reply_text("📥 `Downloading...`")
    try:
        v = Vimeo(input)
        stream = v.streams
        stream[-1].download(download_directory=LOCATION,
                        filename="vimeo.mp4")
        file = "./vimeo.mp4"
        await msg.edit("📤 `Uploading...`")
        cap = f"✨ `Uploaded By:` {user} \n💻 `Bot By:` @FZBOTS"    
        await bot.send_video(message.chat.id, video=file, caption=cap)
        await msg.delete()
        os.remove(file)
    except Exception as e:
        print(str(e))
        await msg.edit("❌ `Error.`")
        return

bot.start()
idle()
