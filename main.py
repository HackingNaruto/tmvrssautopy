import os
import threading
from pyrogram import Client, filters
from flask import Flask

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

SOURCE_CHAT_VAR = os.environ.get("SOURCE_CHAT")
DEST_CHAT_VAR = os.environ.get("DEST_CHAT")

# --- WEB SERVER ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- DEBUG & SETUP ---
print("------------------------------------------------")
print(f"🧐 DEBUG CHECK (Render என்ன ID-ஐ பார்க்கிறது?)")
print(f"👉 Source ID from Env: {SOURCE_CHAT_VAR}")
print(f"👉 Dest Group ID from Env: {DEST_CHAT_VAR}")
print("------------------------------------------------")

# Convert to Integer
try:
    SOURCE_CHAT = int(SOURCE_CHAT_VAR)
    DEST_CHAT = int(DEST_CHAT_VAR)
except ValueError:
    print("❌ Error: ID-கள் நம்பராக இல்லை! Environment Variables-ஐ சரிபார்க்கவும்.")
    exit()

app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

# --- MAIN LOGIC ---
@app.on_message(filters.chat(SOURCE_CHAT))
async def forward_handler(client, message):
    try:
        print(f"📩 Message Received in Source Channel! ID: {message.id}")

        if message.video or message.audio or message.document or message.photo:
            # 1. Forward Message
            print(f"🚀 Forwarding to {DEST_CHAT}...")
            # 'as_copy=True' என்பது முக்கியம்! இது Original Sender ID-ஐ மறைத்துவிடும்.
            # இதுதான் அந்த '-1003621406389' error வராமல் தடுக்கும்.
            forwarded = await message.copy(DEST_CHAT)

            # 2. Reply /ql2
            await client.send_message(
                chat_id=DEST_CHAT,
                text="/ql2",
                reply_to_message_id=forwarded.id
            )
            print("✅ Success! Forwarded & Replied.")
        else:
            print("⚠️ Message is NOT a file.")

    except Exception as e:
        print(f"❌ Error during Forwarding: {e}")

# --- START ---
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
