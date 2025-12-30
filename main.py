import os
import threading
from pyrogram import Client, filters
from flask import Flask

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# ID Handling (Convert String to Integer)
def get_id(val):
    try:
        return int(val)
    except:
        return val

SOURCE_CHAT = get_id(os.environ.get("SOURCE_CHAT"))
DEST_CHAT = get_id(os.environ.get("DEST_CHAT"))

# --- WEB SERVER (Render kaga) ---
app_web = Flask(__name__)

@app_web.route('/')
def home():
    return "Userbot Running Successfully!"

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

print(f"🤖 Userbot Started! Monitoring Source: {SOURCE_CHAT}")

# --- MAIN LOGIC (IDHA MATTUM PAARUNGA) ---
@app.on_message(filters.chat(SOURCE_CHAT))
async def forward_handler(client, message):
    try:
        sent_msg = None
        # Caption irundha eduthukalam, illana Empty
        caption = message.caption or "" 

        # 1. DOCUMENT (Files)
        if message.document:
            print(f"📄 Found Document! Sending by File ID...")
            # Namakku file ID podhum, Original channel theva illa
            sent_msg = await client.send_document(
                chat_id=DEST_CHAT,
                document=message.document.file_id,
                caption=caption
            )

        # 2. VIDEO
        elif message.video:
            print(f"🎥 Found Video! Sending by File ID...")
            sent_msg = await client.send_video(
                chat_id=DEST_CHAT,
                video=message.video.file_id,
                caption=caption
            )

        # 3. AUDIO
        elif message.audio:
            print(f"🎵 Found Audio! Sending by File ID...")
            sent_msg = await client.send_audio(
                chat_id=DEST_CHAT,
                audio=message.audio.file_id,
                caption=caption
            )

        # 4. PHOTO
        elif message.photo:
            print(f"🖼️ Found Photo! Sending by File ID...")
            sent_msg = await client.send_photo(
                chat_id=DEST_CHAT,
                photo=message.photo.file_id,
                caption=caption
            )

        # Reply /ql2
        if sent_msg:
            await client.send_message(
                chat_id=DEST_CHAT,
                text="/ql2",
                reply_to_message_id=sent_msg.id
            )
            print("✅ Sent Successfully & Replied /ql2")

    except Exception as e:
        print(f"❌ Error: {e}")

# --- START ---
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
