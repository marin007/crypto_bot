import logging
import os
import requests
from telegram import Update
from telegram.ext import ApplicationBuilder, CommandHandler, ContextTypes
from dotenv import load_dotenv

# Зареждаме .env файл
load_dotenv()

# Конфигурация
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
CRYPTO_SYMBOL = "bitcoin"

# Логване
logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
                    level=logging.INFO)
logger = logging.getLogger(__name__)

# Команда /start
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Здравей! Аз съм твоят Crypto Alert Bot 🚀")

# Команда /price
async def price(update: Update, context: ContextTypes.DEFAULT_TYPE):
    price = get_crypto_price(CRYPTO_SYMBOL)
    await update.message.reply_text(f"Текуща цена на {CRYPTO_SYMBOL}: ${price}")

# Функция за вземане на цената на криптовалутата
def get_crypto_price(symbol="bitcoin"):
    url = f"https://api.coingecko.com/api/v3/simple/price?ids={symbol.lower()}&vs_currencies=usd"
    
    try:
        # Изпращане на заявка към API-то
        response = requests.get(url)
        
        # Проверка дали заявката е успешна (status code 200)
        if response.status_code == 200:
            data = response.json()
            logging.error(f"API отговор: {url}")  # Логване на отговорите за дебъг
            
            # Проверка дали символът съществува в отговорa
            if symbol.lower() in data:
                # Вземане на цената и форматиране до 2 знака след десетичната запетая
                price = data[symbol.lower()]["usd"]
                formatted_price = "{:,.2f}".format(price)
                return formatted_price
            else:
                logging.error(f"Няма данни за {symbol}. Отговорът е: {data}")
                return f"Няма данни за {symbol}."
        else:
            logging.error(f"Неуспешна заявка към API-то. Код на отговора: {response.status_code}")
            return f"Неуспешна заявка към API-то. Код на отговора: {response.status_code}"
    except Exception as e:
        # Логване на грешки при заявката
        logging.error(f"Грешка при заявката към API-то: {str(e)}")
        return "Възникна грешка при свързването с API-то."

if __name__ == "__main__":
    # Старт на новия ApplicationBuilder API
    app = ApplicationBuilder().token(TOKEN).build()

    # Добавяне на командите
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("price", price))

    # Стартиране на бота
    app.run_polling()
