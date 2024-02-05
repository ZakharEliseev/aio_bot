from datetime import timezone, timedelta, datetime
import httpx
from weather.weather_patterns import (ow_request_url_1d_city,
                                      code_to_smile,
                                      ERROR_CITY_NAME,
                                      ow_request_url_5d_city,
                                      ow_request_url_1d_index,
                                      ow_request_url_5d_index,
                                      )


async def get_weather_ow_1d(city_name):
    response = await ow_request_url_1d_city(city_name)
    if response.status_code == 200:
        try:
            data = response.json()
            city = f"Город: {data['name']}"
            current_temp = f"Температура: {data['main']['temp']}°C"
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Описание: Посмотри в окно, я не понимаю, что там за погода..."
            humidity = f"Влажность: {data['main']['humidity']}%"
            pressure = f"Давление: {data['main']['pressure'] // 1.333} мм.рт.ст"
            wind = f'Скорость ветра: {data["wind"]["speed"]} м/с'
            time_zone = f"Дата запроса: {datetime.now(timezone(timedelta(seconds=data['timezone']))).strftime('%H:%M, %d-%m-%Y')}"
            service_name = '<i>По данным OpenWeather</i>\n'
            return f'{time_zone}\n{city}\n{current_temp}\n{wd}\n{humidity}\n{pressure}\n{wind}\n{service_name}'
        except Exception as e:
            return str(e) + ERROR_CITY_NAME
    else:
        return f"{response.status_code}"


async def get_weather_ow_5d(city_name):
    response = await ow_request_url_5d_city(city_name)
    if response.status_code == 200:
        data = response.json()
        result = []
        service_name = '<i>По данным OpenWeather</i>\n'
        time_zone_current = f"Текущая дата: {datetime.now(timezone(timedelta(seconds=data['city']['timezone']))).strftime('%H:%M, %d-%m-%Y')}"
        result.append(time_zone_current)
        city = f"Город: {data['city']['name']}\n"
        result.append(city)
        for i in range(len(data["list"]) - 26):
            time_zone = f"Дата прогноза: {data['list'][i]['dt_txt']}"
            result.append(time_zone)
            current_temp = f"Температура {data['list'][i]['main']['temp']}°C"
            result.append(current_temp)
            weather_description = data["list"][i]["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = f"{code_to_smile[weather_description]}\n"
                result.append(wd)
            else:
                wd = "Описание: Посмотри в окно, я не понимаю, что там за погода...\n"
                result.append(wd)
        result.append(service_name)
        return '\n'.join(result)


async def get_weather_ow_1d_index(index):
    response = await ow_request_url_1d_index(index)
    if response.status_code == 200:
        try:
            data = response.json()
            city = f"Город: {data['name']}"
            current_temp = f"Температура: {data['main']['temp']}°C"
            weather_description = data["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = code_to_smile[weather_description]
            else:
                wd = "Описание: Посмотри в окно, я не понимаю, что там за погода..."
            humidity = f"Влажность: {data['main']['humidity']}%"
            pressure = f"Давление: {data['main']['pressure'] // 1.333} мм.рт.ст"
            wind = f'Скорость ветра: {data["wind"]["speed"]} м/с'
            time_zone = f"Дата запроса: {datetime.now(timezone(timedelta(seconds=data['timezone']))).strftime('%H:%M, %d-%m-%Y')}"
            service_name = '<i>По данным OpenWeather</i>\n'
            return f'{time_zone}\n{city}\n{current_temp}\n{wd}\n{humidity}\n{pressure}\n{wind}\n{service_name}'
        except Exception as e:
            return str(e) + ERROR_CITY_NAME
    else:
        return f"{response.status_code}"


async def get_weather_ow_5d_index(index):
    response = await ow_request_url_5d_index(index)
    if response.status_code == 200:
        data = response.json()
        result = []
        service_name = '<i>По данным OpenWeather</i>\n'
        time_zone_current = f"Текущая дата: {datetime.now(timezone(timedelta(seconds=data['city']['timezone']))).strftime('%H:%M, %d-%m-%Y')}"
        result.append(time_zone_current)
        city = f"Город: {data['city']['name']}\n"
        result.append(city)
        for i in range(len(data["list"]) - 26):
            time_zone = f"Дата прогноза: {data['list'][i]['dt_txt']}"
            result.append(time_zone)
            current_temp = f"Температура {data['list'][i]['main']['temp']}°C"
            result.append(current_temp)
            weather_description = data["list"][i]["weather"][0]["main"]
            if weather_description in code_to_smile:
                wd = f"{code_to_smile[weather_description]}\n"
                result.append(wd)
            else:
                wd = "Описание: Посмотри в окно, я не понимаю, что там за погода...\n"
                result.append(wd)
        result.append(service_name)
        return '\n'.join(result)
