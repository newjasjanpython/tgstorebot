from loader import bot
from auth0 import ADMINS


async def notify_admins(*args, **kwargs):
  for admin in ADMINS:
    await bot.send_message(admin, *args, **kwargs)
