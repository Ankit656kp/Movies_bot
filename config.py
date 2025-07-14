import os

API_ID = int(os.getenv("API_ID"))
API_HASH = os.getenv("API_HASH")
BOT_TOKEN = os.getenv("BOT_TOKEN")
MONGO_DB_URI = os.getenv("MONGO_DB_URI")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL"))
OWNER_ID = int(os.getenv("OWNER_ID"))

# ✅ New additions (fix for your current error)
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "https://t.me/your_support_group")
BOT_USERNAME = os.getenv("BOT_USERNAME", "your_bot_username")  # without @
