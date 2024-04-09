from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from helpers import get_data, generate_text,error_message,bot_username
@Client.on_callback_query()
async def recheck_pnr(client, callback_query):
    pnr = callback_query.data
    response = await get_data(pnr)
    if response['status']['result'] == "success":
        text = await generate_text(response)
        share_url = "https://t.me/{}?start={}".format(bot_username, pnr)
        await callback_query.edit_message_text(text,
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
        await callback_query.edit_message_text(error_message.format(response['status']['message']['title'], response['status']['message']['message']))