"""
MIT License

Copyright (c) 2021 TheHamkerCat

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""
import asyncio
import importlib
import re

import uvloop
from pyrogram import filters, idle
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup

from wbb import (BOT_NAME, BOT_USERNAME, LOG_GROUP_ID, USERBOT_NAME,
                 aiohttpsession, app, app2)
from wbb.modules import ALL_MODULES
from wbb.modules.sudoers import bot_sys_stats
from wbb.utils import paginate_modules
from wbb.utils.dbfunctions import clean_restart_stage

loop = asyncio.get_event_loop()

HELPABLE = {}


async def start_bot():
    print("[INFO]: BOT BAŞLADILDI")
    await app.start()
    print("[INFO]: USERBOT BAŞLADILDI")
    await app2.start()
    for module in ALL_MODULES:
        imported_module = importlib.import_module(
            "wbb.modules." + module
        )
        if (
            hasattr(imported_module, "__MODULE__")
            and imported_module.__MODULE__
        ):
            imported_module.__MODULE__ = imported_module.__MODULE__
            if (
                hasattr(imported_module, "__HELP__")
                and imported_module.__HELP__
            ):
                HELPABLE[
                    imported_module.__MODULE__.lower()
                ] = imported_module
    bot_modules = ""
    j = 1
    for i in ALL_MODULES:
        if j == 4:
            bot_modules += "|{:<15}|\n".format(i)
            j = 0
        else:
            bot_modules += "|{:<15}".format(i)
        j += 1
    print(
        "+===============================================================+"
    )
    print(
        "|                             AGA MİRZE                         |"
    )
    print(
        "+===============+===============+===============+===============+"
    )
    print(bot_modules)
    print(
        "+===============+===============+===============+===============+"
    )
    print(f"[INFO]: BOT BAŞLADILDI {BOT_NAME}!")
    print(f"[INFO]: BOT BAŞLADILDI {USERBOT_NAME}!")
    restart_data = await clean_restart_stage()
    try:
        print("[INFO]: ONLINE STATUSUN GÖNDƏRİLMƏSİ")
        if restart_data:
            await app.edit_message_text(
                restart_data["chat_id"],
                restart_data["message_id"],
                "**Uğurla yenidən başladın**",
            )

        else:
            await app.send_message(LOG_GROUP_ID, "Bot Başladıldı!")
    except Exception:
        pass
    await idle()
    print("[INFO]: BOTUN DAYANDIRILMASI VƏ AIOHTTP SESSİYASININ QAPANILMASI")
    await aiohttpsession.close()


home_keyboard_pm = InlineKeyboardMarkup(
    [
        [
            InlineKeyboardButton(
                text="kamandalar ❓", callback_data="bot_commands"
            ),
            InlineKeyboardButton(
                text="Sahibim 👱‍♂️ ",
                url="https://t.me/Ayxxan",
            ),
        ],
        [
            InlineKeyboardButton(
                text="Sistem Statistikaları 🖥",
                callback_data="stats_callback",
            ),
            InlineKeyboardButton(
                text="Dəstək 👨", url="http://t.me/nakhidchat"
            ),
        ],
        [
            InlineKeyboardButton(
                text="Məni Qrupa Əlavə Et ➕",
                url=f"http://t.me/{BOT_USERNAME}?startgroup=new",
            )
        ],
    ]
   InlineKeyboardButton(
                text="Tərcümə 👽", url="http://t.me/TheZahid"
)
    ],
       ]

home_text_pm = (
    f"Salam Dostum! Mənim adım {BOT_NAME}. Sənin qrupunu idarə edə bilərəm "
    + "çox faydalı xüsusiyyətlərə malik botam "
    + "məni öz qrupuna əlavə et."
)


@app.on_message(filters.command(["help", "start"]))
async def help_command(_, message):
    if message.chat.type != "private":
        keyboard = InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton(
                        text="Kömək ❓",
                        url=f"t.me/{BOT_USERNAME}?start=help",
                    ),
                    InlineKeyboardButton(
                        text="Sahibim 👱‍♂️",
                        url="https://t.me/Ayxxan",
                    ),
                ],
                [
                    InlineKeyboardButton(
                        text="Sistem Statistikaları 💻",
                        callback_data="stats_callback",
                    ),
                    InlineKeyboardButton(
                        text="Dəstək 👨", url="t.me/Nakhidchat"
                    ),
                ],
            ]
        )
        return await message.reply(
            "Ətraflı məlumat üçün Pm.", reply_markup=keyboard
        )
    await message.reply(
        home_text_pm,
        reply_markup=home_keyboard_pm,
    )


async def help_parser(name, keyboard=None):
    if not keyboard:
        keyboard = InlineKeyboardMarkup(
            paginate_modules(0, HELPABLE, "help")
        )
    return (
        """Salam {first_name}, Mənim adım {bot_name}.
Mən bir çox xüsusiyyətlərə malik olan qrup idarə botuyam.
Bir düyməni basaraq aşağıdan bir seçim seçə bilərsiniz.
Həm də Dəstək Qrupundan istədiyiniz hər şeyi soruşa bilərsiniz.
""".format(
            first_name=name,
            bot_name=BOT_NAME,
        ),
        keyboard,
    )


@app.on_callback_query(filters.regex("bot_commands"))
async def commands_callbacc(_, CallbackQuery):
    text, keyboard = await help_parser(
        CallbackQuery.from_user.mention
    )
    await app.send_message(
        CallbackQuery.message.chat.id,
        text=text,
        reply_markup=keyboard,
    )

    await CallbackQuery.message.delete()


@app.on_callback_query(filters.regex("stats_callback"))
async def stats_callbacc(_, CallbackQuery):
    text = await bot_sys_stats()
    await app.answer_callback_query(
        CallbackQuery.id, text, show_alert=True
    )


@app.on_callback_query(filters.regex(r"help_(.*?)"))
async def help_button(client, query):
    home_match = re.match(r"help_home\((.+?)\)", query.data)
    mod_match = re.match(r"help_module\((.+?)\)", query.data)
    prev_match = re.match(r"help_prev\((.+?)\)", query.data)
    next_match = re.match(r"help_next\((.+?)\)", query.data)
    back_match = re.match(r"help_back", query.data)
    create_match = re.match(r"help_create", query.data)
    top_text = f"""
Salam {query.from_user.first_name}, Mənim adım {BOT_NAME}.
Mən bir çox faydalı xüsusiyyətlərə malik qrup idarə botuyam.
Bir düyməni basaraq aşağıdan bir seçim seçə bilərsiniz.
Həm də Dəstək Qrupundan istədiyiniz hər şeyi soruşa bilərsiniz.

Ümumi əmrlər:
 - /start: botu başlat
 - /help: kömək menusunu aç
 """
    if mod_match:
        module = mod_match.group(1)
        text = (
            "{} **{}**:\n".format(
                "kömək budur", HELPABLE[module].__MODULE__
            )
            + HELPABLE[module].__HELP__
        )

        await query.message.edit(
            text=text,
            reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton(
                            "çıx", callback_data="help_back"
                        )
                    ]
                ]
            ),
            disable_web_page_preview=True,
        )
    elif home_match:
        await app.send_message(
            query.from_user.id,
            text=home_text_pm,
            reply_markup=home_keyboard_pm,
        )
        await query.message.delete()
    elif prev_match:
        curr_page = int(prev_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(curr_page - 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif next_match:
        next_page = int(next_match.group(1))
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(next_page + 1, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif back_match:
        await query.message.edit(
            text=top_text,
            reply_markup=InlineKeyboardMarkup(
                paginate_modules(0, HELPABLE, "help")
            ),
            disable_web_page_preview=True,
        )

    elif create_match:
        text, keyboard = await help_parser(query)
        await query.message.edit(
            text=text,
            reply_markup=keyboard,
            disable_web_page_preview=True,
        )

    return await client.answer_callback_query(query.id)


if __name__ == "__main__":
    uvloop.install()
    loop.run_until_complete(start_bot())
