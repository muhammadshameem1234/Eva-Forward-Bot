import os
import logging
import random
import asyncio
from pyrogram import Client, filters
from pyrogram.errors import ChatAdminRequired, FloodWait
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from info import ADMINS, FILE_CAPTION, LOG_CHANNEL, TARGET_CHANNEL, get_size
import re
import json
import base64
logger = logging.getLogger(__name__)

INDEX_FILES = {}

@Client.on_message(filters.command("start") & filters.incoming & ~filters.edited)
async def start(bot, message):    
    if len(message.command) != 2:
        buttons = [[
            InlineKeyboardButton('⚡️ Updates ⚡️', url='https://t.me/mkn_bots_updates'),
            InlineKeyboardButton('🔰 Movie Channel 🔰', url='https://t.me/KCFilmss')
            ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(
            text="""Hello I am a Auto Forward Bot devoloped by @kcfilmss & @mr_MKN I can forward files from a Public/Private Channel to a Public/Private Group/Channel.""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return

    if len(message.command) == 2 and message.command[1] in ["subscribe", "error", "okay", "help"]:
        buttons = [[
            InlineKeyboardButton('⚡️ Updates ⚡️', url='https://t.me/mkn_bots_updates'),
            InlineKeyboardButton('🔰 Movie Channel 🔰', url='https://t.me/KCFilmss')
            ]]
        reply_markup = InlineKeyboardMarkup(buttons)
        await message.reply_text(            
            text="""Hello I am a Auto Forward Bot devoloped by @kcfilmss & @mr_MKN I can forward files from a Public/Private Channel to a Public/Private Group/Channel.""",
            reply_markup=reply_markup,
            parse_mode='html'
        )
        return
    data = message.command[1]
    try:
        pre, file_id = data.split('_', 1)
    except:
        file_id = data
        pre = ""
    if data.split("-", 1)[0] == "BATCH":
        sts = await message.reply("🙂 I am sending files in your TARGET CHANNEL, when it will complete i will notify you via a message. If i am not sending files in your TARGET CHANNEL then check your logs.")
        file_id = data.split("-", 1)[1]
        msgs = INDEX_FILES.get(file_id)
        frwded = 0
        pling = 0
        if not msgs:
            file = await bot.download_media(file_id)
            try: 
                with open(file) as file_data:
                    msgs=json.loads(file_data.read())
            except:
                await sts.edit("FAILED")
                return await bot.send_message(LOG_CHANNEL, "UNABLE TO OPEN FILE.")
            os.remove(file)
            INDEX_FILES[file_id] = msgs
        for msg in msgs:
            title = msg.get("title")
            size=get_size(int(msg.get("size", 0)))
            f_caption=msg.get("caption", "")
            if FILE_CAPTION:
                try:
                    f_caption=FILE_CAPTION.format(file_name= '' if title is None else title, file_size='' if size is None else size, file_caption='' if f_caption is None else f_caption)
                except Exception as e:
                    logger.exception(e)
                    f_caption=''
            if f_caption is None:
                f_caption = f"{title}"
            try:
                await bot.send_cached_media(
                    chat_id=TARGET_CHANNEL,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
                frwded += 1
                pling += 1
            except FloodWait as e:
                await asyncio.sleep(e.x)
                logger.warning(f"Floodwait of {e.x} sec.")
                await bot.send_cached_media(
                    chat_id=TARGET_CHANNEL,
                    file_id=msg.get("file_id"),
                    caption=f_caption,
                    protect_content=msg.get('protect', False),
                    )
                frwded += 1
                pling += 1
            except Exception as e:
                logger.warning(e, exc_info=True)
                continue
            if pling == 1:
                await sts.edit_text(f"╭━━━━━━━━━━━━━━━➣\n┣⪼ᴛᴏᴛᴀʟ ꜰᴏʀᴡᴀʀᴅᴇᴅ :- <code>{frwded}</code>\n╰━━━━━━━━━━━━━━━➣")
                pling -= 1
        await sts.delete()
        await bot.send_message(
            chat_id=message.chat.id,
            text=f"😎 All files have been successfully sent to TARGET CHANNEL, If not sent check your logs.\n\nForwarded:- {frwded}"
            )
        return
