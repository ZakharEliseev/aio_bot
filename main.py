import asyncio
import logging
import os
from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.memory import MemoryStorage
from dotenv import load_dotenv
from bot.help_handlers import bot_commands, bot_weather_service, bot_gm_service, bot_ow_service
from bot_db import BotDB


async def main():
    logging.basicConfig(level=logging.INFO)
    load_dotenv()
    db = BotDB()
    db.create_table_users()
    db.create_table_favorite_cities()
    db.create_table_user_requests()
    bot = Bot(os.getenv("BOT_TOKEN"), parse_mode="HTML")
    dp = Dispatcher(storage=MemoryStorage())
    dp.include_routers(bot_commands.commands_router,
                       bot_weather_service.weather_service_routers,
                       bot_gm_service.gm_service_routers,
                       bot_ow_service.ow_service_routers,
                       )
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
