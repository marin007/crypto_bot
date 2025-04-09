import os
import logging
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Зареждане на .env файла
load_dotenv()

# Конфигурация
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CRYPTO_SYMBOL = "BTC"
ALERT_THRESHOLD_PERCENT = 30  # Примерен праг за известие

# Логване
logging.basicConfig(level=logging.INFO)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравей! Аз съм твоят Crypto Alert Bot 🚀")

async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_crypto_price(CRYPTO_SYMBOL)
    await update.message.reply_text(f"Текуща цена на {CRYPTO_SYMBOL}: ${price}")

def get_crypto_price(symbol="BTC"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
    response = requests.get(url)
    data = response.json()
    return data[symbol.lower()]["usd"]

if __name__ == "__main__":
    app = ApplicationBuilder().token(TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))
    app.run_polling()
