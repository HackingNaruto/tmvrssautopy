import os
import threading
from pyrogram import Client, filters
from flask import Flask

# --- CONFIGURATION ---
API_ID = int(os.environ.get("API_ID"))
API_HASH = os.environ.get("API_HASH")
SESSION_STRING = os.environ.get("SESSION_STRING")

# ID-களை நம்பராக மாற்றிக்கொள்கிறோம்
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
    return "Bot is Running!"

def run_web():
    port = int(os.environ.get("PORT", 8080))
    app_web.run(host='0.0.0.0', port=port)

# --- BOT CLIENT ---
app = Client("my_bot", api_id=API_ID, api_hash=API_HASH, session_string=SESSION_STRING)

print(f"🤖 Bot Started! Listening to configured Source ID: {SOURCE_CHAT}")

# --- SPY HANDLER (எல்லா மெசேஜையும் பார்க்கும்) ---
@app.on_message(filters.all) 
async def debug_handler(client, message):
    # 1. எந்த Channel-ல் இருந்து மெசேஜ் வந்தாலும் Log-ல் காட்டும்
    print(f"👀 Message Received from Chat ID: {message.chat.id} | Type: {message.chat.type}")

    # 2. Check if it matches your SOURCE_CHAT
    if message.chat.id == SOURCE_CHAT:
        print("✅ ID Matched! Processing File...")
        
        if message.video or message.audio or message.document or message.photo:
            print(f"📩 Forwarding File: {message.id}")
            try:
                forwarded = await message.forward(DEST_CHAT)
                await client.send_message(DEST_CHAT, "/ql2", reply_to_message_id=forwarded.id)
                print("✅ Forwarded & Replied /ql2")
            except Exception as e:
                print(f"❌ Error Forwarding: {e}")
        else:
            print("⚠️ Message is NOT a File (Text only). Ignoring.")
    
    elif message.chat.id == DEST_CHAT:
        pass # Destination group messages ignore
    
    else:
        # ID Match ஆகலனா, உண்மையான ID என்னனு இது சொல்லிரும்
        print(f"⚠️ Mismatch! You posted in {message.chat.id}, but Bot is looking for {SOURCE_CHAT}")

# --- RUN ---
if __name__ == "__main__":
    threading.Thread(target=run_web).start()
    app.run()
