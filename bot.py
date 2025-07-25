# Combined bot.py (autogenerated)

# --- Begin config.py ---
import os

API_ID = int(os.getenv("API_ID", "12345678"))  # Replace with your actual API_ID
API_HASH = os.getenv("API_HASH", "your_api_hash")
BOT_TOKEN = os.getenv("BOT_TOKEN", "your_bot_token")
MONGO_DB_URI = os.getenv("MONGO_DB_URI", "your_mongodb_uri")
LOG_CHANNEL = int(os.getenv("LOG_CHANNEL", "-1001234567890"))
OWNER_ID = int(os.getenv("OWNER_ID", "123456789"))
FORCE_SUB = os.getenv("FORCE_SUB", "YourChannelUsername")
SUPPORT_GROUP = os.getenv("SUPPORT_GROUP", "SupportGroupUsername")
BOT_USERNAME = os.getenv("BOT_USERNAME", "YourBotUsername")
# --- End config.py ---


# --- Begin database/mongo.py ---
from pymongo import MongoClient
from config import MONGO_DB_URI

client = MongoClient(MONGO_DB_URI)
db = client["MovieDownloader"]
users = db["users"]
# --- End database/mongo.py ---


# --- Begin plugins/logger.py ---
from config import LOG_CHANNEL
from pyrogram import Client, filters
from pyrogram.types import Message

@Client.on_message(filters.private & filters.incoming)
async def log_private_messages(client: Client, message: Message):
    try:
        await client.send_message(
            chat_id=LOG_CHANNEL,
            text=f"#PM\n\nFrom: [{message.from_user.first_name}](tg://user?id={message.from_user.id})\nUserID: `{message.from_user.id}`\n\nMessage: {message.text}"
        )
    except Exception:
        pass
# --- End plugins/logger.py ---


# --- Begin plugins/start.py ---
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from config import SUPPORT_GROUP, BOT_USERNAME, OWNER_ID

@Client.on_message(filters.command("start") & filters.private)
async def start_cmd(client, message):
    keyboard = InlineKeyboardMarkup(
        [
            [InlineKeyboardButton("Search Bot 🔍", url=f"https://t.me/{BOT_USERNAME}")],
            [InlineKeyboardButton("Help", callback_data="help")],
            [InlineKeyboardButton("Support", url=f"https://t.me/{SUPPORT_GROUP}")],
        ]
    )
    await message.reply_text(
        f"Hi {message.from_user.mention},\n\nI am a Movie/Webseries Downloader Bot. Just send me the name and I'll try to get it for you!",
        reply_markup=keyboard,
    )
# --- End plugins/start.py ---


# --- Begin plugins/forwarder.py ---
from pyrogram import Client, filters
from pyrogram.types import Message
import asyncio

@Client.on_message(filters.private & filters.text & ~filters.command("start"))
async def forward_user_message(client: Client, message: Message):
    try:
        response = await client.send_message("@Nsi6w8wbot", message.text)
        await asyncio.sleep(5)  # Wait for response
        async for resp in client.get_chat_history("@Nsi6w8wbot", limit=1):
            await resp.copy(message.chat.id)
    except Exception as e:
        await message.reply_text("Something went wrong while forwarding your request.")
# --- End plugins/forwarder.py ---


# --- Begin plugins/admin.py ---
from pyrogram import Client, filters
from config import OWNER_ID
from database.mongo import users
from pyrogram.types import Message

@Client.on_message(filters.command("stats") & filters.user(OWNER_ID))
async def stats(_, message: Message):
    total_users = users.count_documents({})
    await message.reply_text(f"Total users: {total_users}")

@Client.on_message(filters.command("broadcast") & filters.user(OWNER_ID))
async def broadcast(_, message: Message):
    if not message.reply_to_message:
        return await message.reply("Reply to a message to broadcast.")
    total = 0
    failed = 0
    async for user in users.find():
        try:
            await _.send_message(user["user_id"], message.reply_to_message.text)
            total += 1
        except:
            failed += 1
    await message.reply(f"Broadcasted to {total} users.\nFailed: {failed}")
# --- End plugins/admin.py ---


# --- Begin main.py ---
from pyrogram import Client
from config import API_ID, API_HASH, BOT_TOKEN
import asyncio
from database.mongo import users
from pyrogram.types import Message
from pyrogram import filters

app = Client(
    "movie_downloader_bot",
    api_id=API_ID,
    api_hash=API_HASH,
    bot_token=BOT_TOKEN
)

@app.on_message(filters.private)
async def save_user(client, message: Message):
    if not users.find_one({"user_id": message.from_user.id}):
        users.insert_one({"user_id": message.from_user.id})

if __name__ == "__main__":
    print("Bot started...")
    app.run()
# --- End main.py ---
