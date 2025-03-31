from aiogram.filters.command import Command
from aiogram.types import Message
from loader import dp, db
import uuid


__all__ = []


@dp.message(Command('register'))
async def register_bot_handler(msg: Message):
  _, chat_id = msg.text.split()
  try:
    chat_id = int(chat_id)
    status_message = await msg.answer("Creating new storage", parse_mode='markdown')
    
    storage_guid = str(uuid.uuid4())
    await db.execute("""INSERT OR REPLACE INTO storage (guid, chat_id) VALUES (?, ?);""", (storage_guid, chat_id))
    
    await status_message.edit_text(
      f"Storage created [UUID]: || {storage_guid} ||",
      parse_mode='markdown'
    )

  except Exception as err:
    await msg.answer(f"Error: {err.__class__.__name__}: {err}")
