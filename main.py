from loader import db, dp, app, bot
from utils.bot import notify_admins
import logging
import asyncio

from web import *
from bot import *

logging.basicConfig(level=logging.INFO)


@app.on_event("startup")
async def init_db():
  await db.execute("""CREATE TABLE IF NOT EXISTS storage (
    guid varchar(36) PRIMARY KEY UNIQUE,
    chat_id INTEGER UNIQUE
  )""")
  await db.execute("""CREATE TABLE IF NOT EXISTS records (
    guid varchar(36) PRIMARY KEY UNIQUE,
    storage varchar(36),
    status INTEGER DEFAULT 0,
    message_id INTEGER,
    FOREIGN KEY(storage) REFERENCES storage(storage)
  )""")

  if not app.debug:
    await notify_admins(text="Web project is not avaible")

  asyncio.create_task(dp.start_polling(bot), name="DISPATCHERING BOT")
