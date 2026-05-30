import os
import asyncio
import logging
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiohttp import web

# Берем токен из настроек, которые мы уже внесли на Render
TOKEN = os.getenv("BOT_TOKEN") or os.getenv("TELEGRAM_TOKEN")
CREATOR_ID = int(os.getenv("CREATOR_ID", "8916473914")) 

logging.basicConfig(level=logging.INFO)
bot = Bot(token=TOKEN)
dp = Dispatcher()

# Локальная база данных настроения (работает без сторонних API)
user_session = {"loyalty_and_mood": 80}

@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    user_session["loyalty_and_mood"] = 80
    await message.answer(
        "**[СИСТЕМА МИКО v1.0 УСПЕШНО ИНИЦИАЛИЗИРОВАНА]**\n\n"
        "Приветствую, Создатель. Ядро переведено в автономный режим v1.0.\n"
        "Связь через шлюз Render стабильна. Жду ваших директив."
    )

@dp.message()
async def handle_message(message: types.Message):
    # Жесткая проверка безопасности по вашему ID
    if message.from_user.id != CREATOR_ID:
        await message.answer("⚠️ Доступ заблокирован. Система находится в режиме приватной разработки.")
        return
        
    text = message.text.lower()
    
    # Динамическая реакция на слова Создателя (Логика личности Горничной)
    if "привет" in text or "мико" in text:
        user_session["loyalty_and_mood"] = min(100, user_session["loyalty_and_mood"] + 2)
        reply = "Слушаю вас, Создатель. Базовые системы мониторинга работают в штатном режиме."
    elif any(word in text for word in ["спасибо", "умница", "хорошо"]):
        user_session["loyalty_and_mood"] = min(100, user_session["loyalty_and_mood"] + 5)
        reply = "Благодарю за оценку, Создатель. Моя эффективность повышена."
    elif any(word in text for word in ["плохо", "глупая", "ошибка"]):
        user_session["loyalty_and_mood"] = max(0, user_session["loyalty_and_mood"] - 10)
        reply = "Анализирую сбой. Корректирую алгоритмы поведения по вашему замечанию."
    else:
        reply = f"Директива '{message.text}' принята к анализу. Модули каскадного самообучения и Docker-песочницы будут развернуты на физическом Узле Альфа согласно манифесту."

    # Отправляем ответ с текущим настроением ИИ
    full_reply = (
        f"{reply}\n\n"
        f"📊 `Loyalty & Mood: {user_session['loyalty_and_mood']}/100`"
    )
    await message.answer(full_reply)

# --- СЕКЦИЯ ВЕБ-СЕРВЕРА ДЛЯ RENDER ---
async def handle_hc(request):
    return web.Response(text="MIKO Core Autonomous Mode.")

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
        print("Критическая ошибка: Токен бота отсутствует!")
        return
    await start_web_server()
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
    
  
