from helpers import get_data, generate_text,error_message,bot_username
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup



start_text = """
👋 Hello {},

I'm your trusty Unofficial PNR Checker Bot 🤖

Need to check your 🚆 PNR status? Look no further!

Just share your 10-digit PNR number with me, and I'll swiftly fetch the details for you.

Created by @iamyss
"""

@Client.on_message(filters.command("start"))
async def start(client, message):
    await message.reply_text(
        start_text.format(message.from_user.mention),
        reply_markup=InlineKeyboardMarkup(
            [
                [
                    InlineKeyboardButton("👨‍💻 Developer", url="https://t.me/iamyss")
                ],
                [
                    InlineKeyboardButton("🔍 Supported Channel", url="https://t.me/yssprojects")
                ]
            ]
        )
    )
    if len(message.command)>1:
        pnr = message.command[1]
        response = await get_data(pnr)
        if response['status']['result'] == "success":
            text = await generate_text(response)
            share_url = "https://t.me/{}?start={}".format(bot_username, pnr)
            await message.reply_text(text,
                                    reply_markup=InlineKeyboardMarkup(
                    [
                        [
                            InlineKeyboardButton("🔍 Recheck", callback_data=f"{pnr}")
                        ],
                        [
                            InlineKeyboardButton("📤Tg Share", url=f"https://t.me/share/url?url={share_url}&text=Check Your PNR Status Using This Link".replace(" ", '%20')),
                            InlineKeyboardButton("📤Whatsapp Share", url=f"https://api.whatsapp.com/send?text=Check Your PNR Status Using This Link {share_url}".replace(" ", '%20'))
                        ]
                    ]
                ))
        else:
            await message.reply_text(error_message.format(response['status']['message']['title'], response['status']['message']['message']))

@Client.on_message(filters.regex(r"\d{10}"))
async def pnr(client, message):
    pnr = message.text.strip()
    response = await get_data(pnr)
    if response['status']['result'] == "success":
        text = await generate_text(response)
        share_url = "https://t.me/{}?start={}".format(bot_username, pnr)
        await message.reply_text(text,
                                 reply_markup=InlineKeyboardMarkup(
                [
                    [
                        InlineKeyboardButton("🔍 Recheck", callback_data=f"{pnr}")
                    ],
                    [
                        InlineKeyboardButton("📤Tg Share", url=f"https://t.me/share/url?url={share_url}&text=Check Your PNR Status Using This Link".replace(" ", '%20')),
                        InlineKeyboardButton("📤Whatsapp Share", url=f"https://api.whatsapp.com/send?text=Check Your PNR Status Using This Link {share_url}".replace(" ", '%20'))
                    ]
                ]
            ))
    else:
        await message.reply_text(error_message.format(response['status']['message']['title'], response['status']['message']['message']))