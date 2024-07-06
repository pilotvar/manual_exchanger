import os

from dotenv import load_dotenv

load_dotenv()

APP_DEBUG = os.getenv('APP_DEBUG')
APP_NAME = os.getenv('APP_NAME')
BOT_TECH_HOST = os.getenv('BOT_TECH_HOST')


BOT_TOKEN = os.getenv('BOT_TOKEN')
SUPPORT_CHAT_ID = int(os.getenv('SUPPORT_CHAT_ID'))

WEBHOOK_PATH_TECH = f"/tech/"
WEBHOOK_URL_TECH = BOT_TECH_HOST + WEBHOOK_PATH_TECH

POSTGRES_HOST = os.getenv('POSTGRES_HOST')
POSTGRES_PORT = os.getenv('POSTGRES_PORT')
POSTGRES_DB = os.getenv('POSTGRES_DB')
POSTGRES_USER = os.getenv('POSTGRES_USER')
POSTGRES_PASSWORD = os.getenv('POSTGRES_PASSWORD')

REDIS_HOST = os.getenv('REDIS_HOST')
REDIS_PORT = os.getenv('REDIS_PORT')
REDIS_DB = os.getenv('REDIS_DB')

COINMARKET_URL = os.getenv('COINMARKET_URL')
COINMARKET_API = os.getenv('COINMARKET_API')

CURRENCIES = {
    "RUB": "₽",
    "UAH": "₴",
    "KZT": "₸",
    "USD": "$",
    "PLN": "zł",
}

path_errors = 'logs'
