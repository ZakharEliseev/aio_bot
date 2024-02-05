from aiogram import types, F, Router
from aiogram.filters import StateFilter
from aiogram.fsm.context import FSMContext
from aiogram.enums import ParseMode
from bot.keyboards.kbs import inline_kbs_gm_weather_geo, kbs_back, kbs_weather_last_request
from bot.bot_states import ServiceGM
from weather.get_gm_weather import (get_cities_id_gm,
                                    get_weather_gm_city_id,
                                    get_weather_gm_city_id_n_d
                                    )
from aiogram.types import FSInputFile
from bot_db import BotDB

gm_service_routers = Router()
db = BotDB()


@gm_service_routers.callback_query(StateFilter(None), F.data.lower() == "gismeteo")
async def get_weather_for_gm(callback: types.CallbackQuery, state: FSMContext):
    inline_keyboards = types.InlineKeyboardMarkup(inline_keyboard=inline_kbs_gm_weather_geo())
    keyboard = kbs_weather_last_request()
    try:
        city = db.get_last_request(user_id=callback.from_user.id, service_name='gm')
    except TypeError:
        city = 'запросов не было'
    await callback.message.answer('Искать доступные метеостанции или вернуться назад:',
                                  reply_markup=inline_keyboards)
    await callback.message.answer(text=f'Для повтора последнего '
                                       f'запроса воспользуйтесь кнопками под коном ввода сообщений.\n'
                                       f'Ваш последний запрос в GisMeteo был для населенного пункта: '
                                       f'<code>{city}</code>.',
                                  reply_markup=keyboard)
    await state.set_state(ServiceGM.choosing_service_step_1)


@gm_service_routers.message(ServiceGM.choosing_service_step_1, F.text)
async def send_last_query_gm(message: types.Message, state: FSMContext):
    await state.update_data(chosen_request=message.text.lower())
    user_data = await state.get_data()
    user_request = user_data.get('chosen_request', '')
    if user_request == 'последний запрос на текущий прогноз' and state != ServiceGM.choosing_service_step_1:
        try:
            city = db.get_last_request(message.from_user.id, service_name='gm')
            weather_data = await get_weather_gm_city_id(city)
            photo = FSInputFile('gm.jpg')
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
    elif user_request == 'последний запрос на прогноз наперед' and state != ServiceGM.choosing_service_step_1:
        try:
            city = db.get_last_request(message.from_user.id, service_name='gm')
            weather_data = await get_weather_gm_city_id_n_d(city)
            photo = FSInputFile('gm.jpg')
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


@gm_service_routers.callback_query(ServiceGM.choosing_service_step_1, F.data.lower() == 'gm_search_cities_1_d')
async def get_cities_gm(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название города для текущего прогноза:')
    await state.set_state(ServiceGM.choosing_service_step_3_1)


@gm_service_routers.callback_query(ServiceGM.choosing_service_step_1, F.data.lower() == 'gm_search_cities_n_d')
async def get_cities_gm(callback: types.CallbackQuery, state: FSMContext):
    await callback.message.answer('Введите название города для прогноза наперед:')
    await state.set_state(ServiceGM.choosing_service_step_3_2)


@gm_service_routers.message(ServiceGM.choosing_service_step_3_1, F.text)
async def send_searched_cities_gm(message: types.Message, state: FSMContext):
    city = message.text
    cities_data = await get_cities_id_gm(city)
    await state.update_data({'city_name': city})
    await message.answer(cities_data)
    await state.set_state(ServiceGM.choosing_service_step_4_1)


@gm_service_routers.message(ServiceGM.choosing_service_step_3_2, F.text)
async def send_searched_cities_gm(message: types.Message, state: FSMContext):
    city = message.text
    cities_data = await get_cities_id_gm(city)
    await message.answer(cities_data)
    await state.set_state(ServiceGM.choosing_service_step_4_2)


@gm_service_routers.message(ServiceGM.choosing_service_step_4_1, F.text)
async def send_weather_1d_gm(message: types.Message, state: FSMContext):
    city = message.text.replace('/', '')
    db.add_last_request(user_id=message.from_user.id, city=city, service_name='gm')
    db.connection.commit()
    weather_data = await get_weather_gm_city_id(city)
    photo = FSInputFile('gm.jpg')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
    await message.answer_photo(
        photo,
        caption=weather_data,
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )
    await state.clear()


@gm_service_routers.message(ServiceGM.choosing_service_step_4_2, F.text)
async def send_weather_forecast_gm(message: types.Message, state: FSMContext):
    city = message.text.replace('/', '')
    db.add_last_request(user_id=message.from_user.id, city=city, service_name='gm')
    db.connection.commit()
    weather_data = await get_weather_gm_city_id_n_d(city)
    photo = FSInputFile('gm.jpg')
    kb = types.InlineKeyboardMarkup(inline_keyboard=kbs_back())
    await message.answer_photo(
        photo,
        caption=weather_data,
        parse_mode=ParseMode.HTML,
        reply_markup=kb
    )
    await state.clear()
