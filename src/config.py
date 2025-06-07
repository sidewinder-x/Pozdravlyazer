import os
from pathlib import Path
from dotenv import load_dotenv

# --- Умный поиск файла .env ---
# Этот код находит путь к файлу config.py, поднимается на одну папку вверх (в корень проекта)
# и ищет там файл .env. Это самый надежный способ.
env_path = Path(__file__).parent.parent / '.env'
load_dotenv(dotenv_path=env_path)

# --- Telegram Bot Token ---
BOT_TOKEN = os.getenv("BOT_TOKEN")
if not BOT_TOKEN:
    raise ValueError("BOT_TOKEN is not set in the .env file")

# --- Channel for Subscription Check ---
CHANNEL_ID = os.getenv("CHANNEL_ID")
CHANNEL_URL = os.getenv("CHANNEL_URL")
if not CHANNEL_ID or not CHANNEL_URL:
    raise ValueError("CHANNEL_ID and CHANNEL_URL must be set for subscription check")

# --- YandexGPT API Keys ---
YANDEX_API_KEY = os.getenv("YANDEX_API_KEY")
YANDEX_FOLDER_ID = os.getenv("YANDEX_FOLDER_ID")

# Эта проверка - причина вашей ошибки. Она сработает, если .env не найден.
if not YANDEX_API_KEY or not YANDEX_FOLDER_ID:
    raise ValueError("YANDEX_API_KEY and YANDEX_FOLDER_ID must be set for AI generation")
