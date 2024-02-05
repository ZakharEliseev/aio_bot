import asyncio
import json
import os
import httpx
from dotenv import load_dotenv


async def ow_request_url_1d_city(city):
    load_dotenv()
    city_name = city.lower()
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={os.getenv('OPENWEATHER_TOKEN')}&units"
        f"=metric&lang=ru")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, timeout=httpx.Timeout(timeout=10.0, read=30.0))
            return response
        except httpx.ConnectTimeout:
            return "Превышен тайм-аут соединения с OpenWeather"
        except httpx.ReadTimeout:
            return "Превышен тайм-аут ожидания ответа от OpenWeather"


async def ow_request_url_5d_city(city):
    load_dotenv()
    city_name = city.lower()
    url = (
        f"https://api.openweathermap.org/data/2.5/forecast?q={city_name}&appid={os.getenv('OPENWEATHER_TOKEN')}&units"
        f"=metric&lang=ru")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, timeout=httpx.Timeout(timeout=10.0, read=30.0))
            return response
        except httpx.ConnectTimeout:
            return "Превышен тайм-аут соединения с OpenWeather"
        except httpx.ReadTimeout:
            return "Превышен тайм-аут ожидания ответа от OpenWeather"


async def ow_request_url_1d_index(index):
    load_dotenv()
    url = (
        f"https://api.openweathermap.org/data/2.5/weather?zip={index},"
        f"ru&appid={os.getenv('OPENWEATHER_TOKEN')}&units"
        f"=metric&lang=ru")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, timeout=httpx.Timeout(timeout=10.0, read=30.0))
            return response
        except httpx.ConnectTimeout:
            return "Превышен тайм-аут соединения с OpenWeather"
        except httpx.ReadTimeout:
            return "Превышен тайм-аут ожидания ответа от OpenWeather"


async def ow_request_url_5d_index(index):
    load_dotenv()
    url = (f"https://api.openweathermap.org/data/2.5/forecast?zip={index},"
           f"ru&appid={os.getenv('OPENWEATHER_TOKEN')}&units"
           f"=metric&lang=ru")
    async with httpx.AsyncClient() as client:
        try:
            response = await client.get(url=url, timeout=httpx.Timeout(timeout=10.0, read=30.0))
            return response
        except httpx.ConnectTimeout:
            return "Превышен тайм-аут соединения с OpenWeather"
        except httpx.ReadTimeout:
            return "Превышен тайм-аут ожидания ответа от OpenWeather"



async def gm_search_cities(city):
    load_dotenv()
    url = 'https://api.gismeteo.net/v2/search/cities/'
    get_token = os.getenv('GISMETEO_TOKEN')
    headers = {'X-Gismeteo-Token': get_token}
    params = {'query': city}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        return response


async def gm_request_url_1d(city_id):
    load_dotenv()
    url = f'https://api.gismeteo.net/v2/weather/current/{city_id}/'
    get_token = os.getenv('GISMETEO_TOKEN')
    headers = {'X-Gismeteo-Token': get_token}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response


async def gm_request_url_forecast(city_id):
    load_dotenv()
    url = f'https://api.gismeteo.net/v2/weather/forecast/{city_id}/?lang=ru&days=10'
    get_token = os.getenv('GISMETEO_TOKEN')
    headers = {'X-Gismeteo-Token': get_token}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers)
        return response


code_to_smile = {
    "Clear": "Ясно \U00002600",
    "Clouds": "Облачно \U00002601",
    "Rain": "Дождь \U00002614",
    "Drizzle": "Дождь \U00002614",
    "Thunderstorm": "Гроза \U000026A1",
    "Snow": "Снег \U0001F328",
    "Mist": "Туман \U0001F32B"
}

gm_precipitation_type_pattern = {
    '0': 'Нет осадков \U00002600',
    '1': 'Дождь \U00002614',
    '2': 'Снег \U0001F328',
    '3': '🌧 Смешанные осадки 🌤️',
}

gm_description_geomagnetic_pattern = {
    0: 'Все спокойно.',
    1: 'Нет заметных возмущений',
    2: 'Небольшие возмущения',
    3: 'Слабая геомагнитная буря',
    4: 'Малая геомагнитная буря',
    5: 'Умеренная геомагнитная буря',
    6: 'Сильная геомагнитная буря',
    7: 'Жесткий геомагнитный шторм',
    8: 'Экстремальный шторм',
}

ERROR_CITY_NAME = f'Ошибка в названии города '

"""
    for debug and test
"""


async def main():
    print(await ow_request_url_5d_index('628160'))


if __name__ == '__main__':
    asyncio.run(main())
