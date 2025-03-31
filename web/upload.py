import asyncio
from concurrent.futures import ThreadPoolExecutor
from typing import Annotated
from fastapi import File, Form
from aiogram.types import BufferedInputFile, ReactionTypeEmoji
from loader import app, bot, db
import uuid

executor = ThreadPoolExecutor(max_workers=5)

async def send_helper(chat_id, record_guid, storage, upload_file):
  message = await bot.send_document(chat_id, upload_file)
  await message.react([ReactionTypeEmoji(emoji='🔥')])
  await db.execute(
    "INSERT INTO records (guid, storage, message_id) VALUES (?, ?, ?)", 
    (record_guid, storage, message.message_id)
  )

@app.post('/upload/')
async def upload_api_handler(
  file: Annotated[bytes, File()],
  filename: Annotated[str, Form()],
  storage: Annotated[str, Form()]
):
  chat_id = await db.execute("SELECT chat_id FROM storage WHERE guid=?", (storage,), fetch="one")
  if chat_id:
    chat_id = chat_id[0]
    record_guid = str(uuid.uuid4())
    upload_file = BufferedInputFile(file, filename)
    asyncio.create_task(send_helper(chat_id, record_guid, storage, upload_file))

    return {"status": "uploading", "check": record_guid}
  
  return {"status": "error", "details": "No storage with this GUID."}
