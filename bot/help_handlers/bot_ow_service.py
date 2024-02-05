from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from bot.keyboards.kbs import kbs_ow_weather_geo, kbs_back, kbs_weather_last_request
from bot.bot_states import ServiceOW
from weather.get_ow_weather import (get_weather_ow_1d,
                                    get_weather_ow_5d,
                                    get_weather_ow_1d_index,
                                    get_weather_ow_5d_index,
                                    )
from aiogram.types import FSInputFile
from bot_db import BotDB

ow_service_routers = Router()
db = BotDB()


@ow_service_routers.callback_query(StateFilter(None), F.data.lower() == "openweather")
async def get_weather_for_ow(callback: types.CallbackQuery, state: FSMContext):
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_ow_weather_geo())
    keyboard = kbs_weather_last_request()
    try:
        city = db.get_last_request(user_id=callback.from_user.id, service_name='ow')
    except TypeError:
        city = 'запросов не было'
    await callback.message.answer('Выберите дату предоставления прогноза и определение местоположения по данным '
                                  'сервиса openweather:', reply_markup=kb)
    await callback.message.answer(text=f'Для повтора последнего '
                                       f'запроса воспользуйтесь кнопками под коном ввода сообщений.\n'
                                       f'Ваш последний запрос в OpenWeather был для населенного пункта: '
                                       f'<code>{city}</code>.',
                                  reply_markup=keyboard)
    await state.set_state(ServiceOW.choosing_service_step_1)


@ow_service_routers.message(ServiceOW.choosing_service_step_1, F.text)
async def send_last_query_gm(message: types.Message, state: FSMContext):
    await state.update_data(chosen_request=message.text.lower())
    user_data = await state.get_data()
    user_request = user_data.get('chosen_request', '')
    if user_request == 'последний запрос на текущий прогноз' and state != ServiceOW.choosing_service_step_1:
        try:
            city = db.get_last_request(message.from_user.id, service_name='ow')
            weather_data = await get_weather_ow_1d(city) if isinstance(city, str) else await get_weather_ow_1d_index(city)
            photo = FSInputFile('ow.jpg')
            await message.answer_photo(
                photo,
                caption=weather_data,
                parse_mode=ParseMode.HTML,
                reply_markup=types.ReplyKeyboardRemove()
            )
            kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
            await message.answer('Начнем сначала?', reply_markup=kb)
            await state.clear()
        except TypeError:
            await message.answer('Вы еще не делали запросов, история пуста или очищена.')
    elif user_request == 'последний запрос на прогноз наперед' and state != ServiceOW.choosing_service_step_1:
        try:
            city = db.get_last_request(message.from_user.id, service_name='ow')
            weather_data = await get_weather_ow_5d(city) if isinstance(city, str) else await get_weather_ow_5d_index(city)
            photo = FSInputFile('ow.jpg')
            await message.answer_photo(
                photo,
                caption=weather_data,
                parse_mode=ParseMode.HTML,
                reply_markup=types.ReplyKeyboardRemove()
            )
            kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
            await message.answer('Начнем сначала?', reply_markup=kb)
            await state.clear()
        except TypeError:
            await message.answer('Вы еще не делали запросов, история пуста или очищена.')
    else:
        await message.answer('Используйте клавиатуры.',
                             parse_mode=ParseMode.HTML, reply_markup=types.ReplyKeyboardRemove())


@ow_service_routers.callback_query(ServiceOW.choosing_service_step_1, F.data.lower() == 'ow_current_day_city')
async def get_city_for_ow_1d(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Напишите название города для текущего прогноза по данным OpenWeather:')
    await state.set_state(ServiceOW.choosing_service_step_3)


@ow_service_routers.callback_query(ServiceOW.choosing_service_step_1, F.data.lower() == 'ow_5_day_city')
async def get_city_for_ow_5d(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Напишите название города для прогноза на 5 дней по данным OpenWeather:')
    await state.set_state(ServiceOW.choosing_service_step_4)


@ow_service_routers.callback_query(ServiceOW.choosing_service_step_1, F.data.lower() == 'ow_current_day_index')
async def get_index_for_ow_1d(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Напишите почтовый индекс для текущего прогноза по данным OpenWeather:')
    await state.set_state(ServiceOW.choosing_service_step_5)


@ow_service_routers.callback_query(ServiceOW.choosing_service_step_1, F.data.lower() == 'ow_5_day_index')
async def get_index_for_ow_5d(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Напишите почтовый индекс для прогноза на 5 дней по данным OpenWeather')
    await state.set_state(ServiceOW.choosing_service_step_6)


@ow_service_routers.message(ServiceOW.choosing_service_step_3, F.text)
async def send_weather_ow_1d(message: types.Message, state: FSMContext):
    city_name = message.text
    weather_data = await get_weather_ow_1d(city_name)
    photo = FSInputFile('ow.jpg')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
    db.add_last_request(user_id=message.from_user.id, city=city_name, service_name='ow')
    db.connection.commit()
    await message.answer_photo(
        photo,
        caption=weather_data,
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )
    await state.clear()


@ow_service_routers.message(ServiceOW.choosing_service_step_4, F.text)
async def send_weather_ow_5d(message: types.Message, state: FSMContext):
    city_name = message.text
    weather_data = await get_weather_ow_5d(city_name)
    photo = FSInputFile('ow.jpg')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
    db.add_last_request(user_id=message.from_user.id, city=city_name, service_name='ow')
    db.connection.commit()
    await message.answer_photo(
        photo,
        caption=weather_data,
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )
    await state.clear()


@ow_service_routers.message(ServiceOW.choosing_service_step_5, F.text)
async def send_weather_ow_1d_index(message: types.Message, state: FSMContext):
    index = message.text
    weather_data = await get_weather_ow_1d_index(index)
    photo = FSInputFile('ow.jpg')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
    db.add_last_request(user_id=message.from_user.id, city=index, service_name='ow')
    db.connection.commit()
    await message.answer_photo(
        photo,
        caption=weather_data,
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )
    await state.clear()


@ow_service_routers.message(ServiceOW.choosing_service_step_6, F.text)
async def send_weather_ow_5d_index(message: types.Message, state: FSMContext):
    index = message.text
    weather_data = await get_weather_ow_5d_index(index)
    photo = FSInputFile('ow.jpg')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
    db.add_last_request(user_id=message.from_user.id, city=index, service_name='ow')
    db.connection.commit()
    await message.answer_photo(
        photo,
        caption=weather_data,
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )
    await state.clear()
