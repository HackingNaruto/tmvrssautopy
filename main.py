import os
import threading
import asyncio
from pyrogram import Client, filters
from flask import Flask

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# IDs can be environment variables
SOURCE_CHAT_VAR = os.environ.get("SOURCE_CHAT")
DEST_CHAT_VAR = os.environ.get("DEST_CHAT")

# Helper to convert ID to Integer if possible
def get_chat_id(id_val):
    try:
        return int(id_val)
    except:
        return id_val # Returns username string if not a number

SOURCE_CHAT = get_chat_id(SOURCE_CHAT_VAR)
DEST_CHAT = get_chat_id(DEST_CHAT_VAR)

# --- WEB SERVER (To keep Render happy) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is Running Successfully on Render!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- BOT SETUP ---
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

print(f"🚀 Monitoring Source: {SOURCE_CHAT}")
print(f"🚀 Forwarding to: {DEST_CHAT}")

# --- MAIN LOGIC ---
@app.on_message(filters.chat(SOURCE_CHAT))
async def forward_handler(client, message):
    try:
        # Check if message has media
        if message.video or message.audio or message.document or message.photo:
            print(f"📩 New Media Found: {message.id}")

            # 1. Forward to Destination
            forwarded = await message.forward(DEST_CHAT)

            # 2. Reply /ql2
            await client.send_message(
                chat_id=DEST_CHAT,
                text="/ql2",
                reply_to_message_id=forwarded.id
            )
            print("✅ Forwarded & Replied /ql2")
            
    except Exception as e:
        print(f"⚠️ Error: {e}")

# --- STARTUP ---
if __name__ == "__main__":
    # 1. Start Web Server in a separate thread
    t = threading.Thread(target=run_web)
    t.daemon = True
    t.start()

    # 2. Start Bot (Blocking mode)
    print("✅ Bot Started! Waiting for files...")
    app.run()
