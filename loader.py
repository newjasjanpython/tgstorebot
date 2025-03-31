from aiogram import Bot, Dispatcher
from utils.database import Database
from fastapi import FastAPI
import auth0

dp = Dispatcher()
bot = Bot(auth0.BOT_TOKEN)
db = Database('database.db')
app = FastAPI(debug=False)
