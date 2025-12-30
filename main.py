from telethon import TelegramClient, events
from telethon.sessions import StringSession
import asyncio
import os

# Koyeb-ல் இருந்து விபரங்களை எடுக்கும்
api_id = os.environ.get('API_ID')
api_hash = os.environ.get('API_HASH')
session_string = os.environ.get('SESSION_STRING')
source_channel_id = int(os.environ.get('SOURCE_CHANNEL'))
destination_group_id = int(os.environ.get('DEST_GROUP'))

client = TelegramClient(StringSession(session_string), api_id, api_hash)

print("Userbot Started on Cloud...")

@client.on(events.NewMessage(chats=source_channel_id))
async def handler(event):
    if event.message.media or event.message.file:
        try:
            forwarded_msg = await client.forward_messages(destination_group_id, event.message)
            await asyncio.sleep(2)
            await client.send_message(destination_group_id, '/ql2', reply_to=forwarded_msg)
        except Exception as e:
            print(f"Error: {e}")

client.start()
client.run_until_disconnected()
