import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from openai import AsyncOpenAI
from aiohttp import web

TOKEN = os.getenv("TELEGRAM_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
CREATOR_ID = int(os.getenv("CREATOR_ID", "123456789")) 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()
ai_client = AsyncOpenAI(api_key=OPENAI_API_KEY)

user_session = {"loyalty_and_mood": 80, "history": []}

MIKO_SYSTEM_PROMPT = "Ты — MIKO (v1.0), автономная ИИ-система управления. Твой уровень настроения: {mood}/100."

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "**[СИСТЕМА МИКО v1.0 ИНИЦИАЛИЗИРОВАНА]**\n\n"
        "Приветствую, Создатель. Связь через веб-сервер Render успешно установлена. Я готова."
    )

@dp.message()
async def handle_message(message: types.Message):
    if message.from_user.id != CREATOR_ID:
        await message.answer("⚠️ Доступ заблокирован. Режим приватной разработки.")
        return
    await message.answer(f"Принято, Создатель. Система функционирует нормально. Настроение: {user_session['loyalty_and_mood']}/100.")

async def handle_hc(request):
    return web.Response(text="MIKO Core is running perfectly.")

async def start_web_server():
    app = web.Application()
    app.router.add_get("/", handle_hc)
    runner = web.AppRunner(app)
    await runner.setup()
    port = int(os.getenv("PORT", "10000"))
    site = web.TCPSite(runner, "0.0.0.0", port)
    await site.start()

async def main():
    if not TOKEN:
        return
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
  
