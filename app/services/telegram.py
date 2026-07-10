import os
from telegram import Bot


BOT_TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CHANNEL_ID = os.getenv("TELEGRAM_CHANNEL_ID")


async def invia_offerta_testo(testo):
    bot = Bot(token=BOT_TOKEN)

    await bot.send_message(
        chat_id=CHANNEL_ID,
        text=testo
    )