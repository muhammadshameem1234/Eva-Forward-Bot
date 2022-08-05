import os
import sys
import asyncio
from pyrogram import Client, filters

@Client.on_message(filters.private & filters.command(['restart']))
async def restart(bot, message):
    msg = await message.reply_text(
        text="<i>Trying to restarting.....</i>"
    )
    await asyncio.sleep(5)
    await msg.edit("<i>Server restarted successfully ✅</i>")
    os.execl(sys.executable, sys.executable, *sys.argv)