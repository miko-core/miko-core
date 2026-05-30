import os
import asyncio
from fastapi import FastAPI, Request
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.storage.memory import MemoryStorage

# 1. Инициализация. Токен берется из настроек Space
TOKEN = os.getenv("TELEGRAM_BOT_TOKEN")
# Hugging Face автоматически дает имя вашему пространству, строим URL:
SPACE_AUTHOR = os.getenv("SPACE_AUTHOR_NAME")
SPACE_NAME = os.getenv("SPACE_REPO_NAME")
WEBHOOK_URL = f"https://{SPACE_AUTHOR}-{SPACE_NAME}.hf.space/webhook"

bot = Bot(token=TOKEN)
dp = Dispatcher(storage=MemoryStorage())
app = FastAPI()

# 2. Обработчик команд и сообщений (Личность MIKO v1.0)
@dp.message(commands=["start"])
async def send_welcome(message: types.Message):
    await message.reply(
        "✨ Системное ядро MIKO v1.0 активировано.\n"
        "Приветствую, Создатель. Я готова к работе и мониторингу."
    )

@dp.message()
async def echo_all(message: types.Message):
    # Внутренний монолог (упрощенная версия для теста)
    thinking = f"*[Внутренний монолог]: Запрос обработан. Лояльность: 100%.*\n\n"
    reply = f"Я услышала вас, Создатель. Ваш запрос: «{message.text}»"
    await message.reply(thinking + reply, parse_mode="Markdown")

# 3. Настройка маршрутов для Hugging Face
@app.get("/")
def read_root():
    return {"status": "MIKO Core online", "webhook_configured_to": WEBHOOK_URL}

@app.post("/webhook")
async def telegram_webhook(request: Request):
    update = types.Update.model_validate(await request.json(), context={"bot": bot})
    await dp.feed_update(bot, update)

# 4. Регистрация вебхука при запуске сервера
@app.on_event("startup")
async def on_startup():
    await bot.set_webhook(url=WEBHOOK_URL, drop_pending_updates=True)

@app.on_event("shutdown")
async def on_shutdown():
    await bot.delete_webhook()
    
    
  
