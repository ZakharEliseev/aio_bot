from aiogram import types, F, Router
from bot.keyboards.kbs import kbs_weather_menu
from bot_db import BotDB

weather_service_routers = Router()
db = BotDB()


@weather_service_routers.callback_query(F.data.lower() == "weather")
async def choose_weather_service(callback: types.CallbackQuery):
    if not db.user_exists(callback.from_user.id):
        db.add_user(callback.from_user.id, username=callback.from_user.username)
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_weather_menu())
    await callback.message.answer('Выберите сервис предоставления погоды:', reply_markup=kb)
