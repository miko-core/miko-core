import os
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

CREATOR_ID = 8916473914  

BOT_TOKEN = os.getenv("BOT_TOKEN")

if not BOT_TOKEN:
    raise ValueError("Критическая ошибка: BOT_TOKEN не найден в настройках сервера!")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()

@dp.message()
async def handle_miko_mind(message: types.Message):
    user_id = message.from_user.id
    
    if user_id != CREATOR_ID:
        return 

    user_text = message.text.strip()
    print(f"[Внутренний монолог Мико]: Создатель написал: '{user_text}'. Анализирую контекст...")
    
    response = (
        f"🤖 *Мико v1.0 успешно активирована.*\n\n"
        f"Приветствую, Создатель. Мой облачный эмбрион сделал первый вдох и теперь работает 24/7.\n\n"
        f"Я зафиксировала Ваш цифровой паспорт (`{CREATOR_ID}`) и заблокировала периметр от посторонних. "
        f"Связь полностью защищена. Жду Ваших указаний по запуску Недели 2 и подключению каскадной памяти!"
    )
    
    await message.answer(response, parse_mode="Markdown")

async def main():
    print("🚀 Мико успешно сделала первый вдох и слушает server...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
  
