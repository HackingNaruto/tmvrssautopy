import os
import threading
from pyrogram import Client, filters
from flask import Flask

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING") # Userbot String

# ID Handling
def get_id(val):
    try:
        return int(val)
    except:
        return val

SOURCE_CHAT = get_id(os.environ.get("SOURCE_CHAT"))
DEST_CHAT = get_id(os.environ.get("DEST_CHAT"))

# --- WEB SERVER ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Userbot is Running Successfully!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- USERBOT CLIENT ---
app = Client(
    "my_userbot",
    api_id=API_ID,
    api_hash=API_HASH,
    session_string=SESSION_STRING
)

print(f"🤖 Userbot Started! Monitoring: {SOURCE_CHAT}")

# --- MAIN LOGIC (FILE ID METHOD) ---
@app.on_message(filters.chat(SOURCE_CHAT))
async def forward_handler(client, message):
    try:
        sent_msg = None
        caption = message.caption or "" # Caption irundha eduthukum

        # 1. DOCUMENT (Files)
        if message.document:
            print(f"📄 Sending Document: {message.document.file_name}")
            sent_msg = await client.send_document(
                chat_id=DEST_CHAT,
                document=message.document.file_id,
                caption=caption
            )

        # 2. VIDEO
        elif message.video:
            print(f"🎥 Sending Video...")
            sent_msg = await client.send_video(
                chat_id=DEST_CHAT,
                video=message.video.file_id,
                caption=caption
            )

        # 3. AUDIO
        elif message.audio:
            print(f"🎵 Sending Audio...")
            sent_msg = await client.send_audio(
                chat_id=DEST_CHAT,
                audio=message.audio.file_id,
                caption=caption
            )

        # 4. PHOTO
        elif message.photo:
            print(f"🖼️ Sending Photo...")
            sent_msg = await client.send_photo(
                chat_id=DEST_CHAT,
                photo=message.photo.file_id,
                caption=caption
            )

        # Reply /ql2 if file was sent
        if sent_msg:
            await client.send_message(
                chat_id=DEST_CHAT,
                text="/ql2",
                reply_to_message_id=sent_msg.id
            )
            print("✅ Sent as NEW message & Replied /ql2")

    except Exception as e:
        print(f"❌ Error: {e}")

# --- START ---
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
