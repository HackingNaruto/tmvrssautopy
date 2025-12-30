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

def get_id(val):
    try:
        return int(val)
    except:
        return val

SOURCE_CHAT = get_id(SOURCE_CHAT_VAR)
DEST_CHAT = get_id(DEST_CHAT_VAR)

# --- WEB SERVER ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Bot is Running Securely!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- BOT CLIENT ---
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

print(f"🤖 Bot Started! Monitoring: {SOURCE_CHAT}")

# --- MAIN LOGIC ---
@app.on_message(filters.chat(SOURCE_CHAT))
async def forward_handler(client, message):
    try:
        # Check for Media
        if message.video or message.audio or message.document or message.photo:
            print(f"📩 New File Found! ID: {message.id}")

            # -------------------------------------------------------
            # SOLUTION: 'copy' method use panrom. 
            # Idhu original sender ID-a thedaadhu. Direct ah send pannum.
            # -------------------------------------------------------
            print(f"🚀 Copying to Destination ({DEST_CHAT})...")
            
            # MUKKIYAM: forward() ku badhila copy() use panrom
            copied_msg = await message.copy(DEST_CHAT)

            # Reply /ql2 to the copied message
            await client.send_message(
                chat_id=DEST_CHAT,
                text="/ql2",
                reply_to_message_id=copied_msg.id
            )
            print("✅ Success! Copied & Replied /ql2")

    except Exception as e:
        print(f"❌ Error: {e}")

# --- START ---
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
