import logging
import os
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Зареждаме .env файл
load_dotenv()

# Конфигурация
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CRYPTO_SYMBOL = "BTC"

# Логване
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

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
    # Старт на новия ApplicationBuilder API
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавяне на командите
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    # Стартиране на бота
    app.run_polling()
