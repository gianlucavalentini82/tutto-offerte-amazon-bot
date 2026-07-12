import os

from telegram import Bot
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


async def invia_offerta(
    testo,
    link_amazon,
    link_youtube=None,
    foto=None
):

    bot = Bot(token=BOT_TOKEN)

    pulsanti = [
        [
            InlineKeyboardButton(
                "🛒 Acquista su Amazon",
                url=link_amazon
            )
        ]
    ]

    if link_youtube:
        pulsanti.append(
            [
                InlineKeyboardButton(
                    "🎥 Guarda recensione",
                    url=link_youtube
                )
            ]
        )

    pulsanti.append(
        [
            InlineKeyboardButton(
                "📲 Condividi offerta",
                url=f"https://wa.me/?text={link_amazon}"
            )
        ]
    )

    pulsanti.append(
        [
            InlineKeyboardButton(
                "📢 Invita al canale",
                url="https://wa.me/?text=Ti consiglio questo canale Telegram di offerte Amazon: https://t.me/tuttooffert"
            )
        ]
    )

    tastiera = InlineKeyboardMarkup(pulsanti)

    if foto:

        with open(foto, "rb") as immagine:

            await bot.send_photo(
                chat_id=CHANNEL_ID,
                photo=immagine,
                caption=testo,
                reply_markup=tastiera
            )

    else:

        await bot.send_message(
            chat_id=CHANNEL_ID,
            text=testo,
            reply_markup=tastiera
        )