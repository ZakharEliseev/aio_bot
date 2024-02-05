from aiogram import types
from aiogram.types import ReplyKeyboardMarkup
from aiogram.utils.keyboard import ReplyKeyboardBuilder


def kbs_menu():
    buttons = [
        [
            types.InlineKeyboardButton(text='Прогноз погоды', callback_data='weather'),
            types.InlineKeyboardButton(text='Справка по командам', callback_data='show_cmds')
        ]
    ]
    return buttons


def kbs_weather_menu():
    buttons = [
        [
            types.InlineKeyboardButton(text='OpenWeather', callback_data='openweather'),
            types.InlineKeyboardButton(text='GisMeteo', callback_data='gismeteo')
        ],
        [types.InlineKeyboardButton(text='Назад', callback_data='menu')]
    ]
    return buttons


def kbs_ow_weather_geo():
    buttons = [
        [
            types.InlineKeyboardButton(text='сейчас по названию города', callback_data='ow_current_day_city')
        ],
        [
            types.InlineKeyboardButton(text='наперед по названию города', callback_data='ow_5_day_city')
        ],
        [
            types.InlineKeyboardButton(text='сейчас по почтовому индексу', callback_data='ow_current_day_index')
        ],
        [
            types.InlineKeyboardButton(text='наперед по почтовому индексу', callback_data='ow_5_day_index')
        ],
        [types.InlineKeyboardButton(text='Назад', callback_data='menu')]
    ]
    return buttons


def inline_kbs_gm_weather_geo():
    inline_buttons = [
        [
            types.InlineKeyboardButton(text='Текущий прогноз по названию города', callback_data='gm_search_cities_1_d'),
        ],
        [
            types.InlineKeyboardButton(text='Прогноз наперед по названию города', callback_data='gm_search_cities_n_d'),
        ],
        [types.InlineKeyboardButton(text='Назад', callback_data='menu')]
    ]
    return inline_buttons


def kbs_weather_last_request():
    buttons = [
        [
            types.KeyboardButton(text='Последний запрос на текущий прогноз'),
            types.KeyboardButton(text='Последний запрос на прогноз наперед'),
        ]
    ]
    kb = types.ReplyKeyboardMarkup(keyboard=buttons, resize_keyboard=True, one_time_keyboard=True)
    return kb


def kbs_back():
    buttons = [
        [types.InlineKeyboardButton(text='В главное меню', callback_data='menu')],
    ]
    return buttons
