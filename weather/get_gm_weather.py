import asyncio
from weather.weather_patterns import (gm_request_url_forecast,
                                      ERROR_CITY_NAME,
                                      gm_search_cities, gm_request_url_1d, gm_precipitation_type_pattern,
                                      gm_description_geomagnetic_pattern
                                      )


async def get_cities_id_gm(city_name):
    try:
        response = await gm_search_cities(city_name)
        status_code = response.status_code
        if status_code == 200:
            data = response.json()
            if 'error' in data.get('response', {}):
                error_message = data['response']['error']['message']
                error_code = data['response']['error']['code']
                if error_message:
                    return f"Ошибка сервера Gismeteo: {error_message} {error_code}"
                else:
                    return "Неизвестная сервера Gismeteo"
            else:
                cities_name = data['response']['items']
                cities_data = {}
                for i in range(len(cities_name)):
                    cities_data[data['response']['items'][i]['id']] = (
                        f"Область: {data['response']['items'][i]['district']['name']}\n "
                        f"город: {data['response']['items'][i]['name']}")
                result = [f'Нажмите на нужный вам ID города для поиска погоды \nID( /{key} )\n: {value}\n\n' for key, value in cities_data.items()]
                return f"{''.join(result)}"
    except Exception as e:
        return f"Произошла ошибка: {e}"
    return f"{response.status_code}"


async def get_weather_gm_city_id(city_id):
    response = await gm_request_url_1d(city_id)
    status_code = response.status_code
    if status_code == 200:
        try:
            data = response.json()
            date = f'Дата прогноза: {data["response"]["date"]["local"]}\n'
            emoji_temp = f'🌡Сведения о температуре🌡: \n'
            temp_air = f"Температура воздуха: {data['response']['temperature']['air']['C']}°C\n"
            temp_comfort = f"Температура по ощущению: {data['response']['temperature']['comfort']['C']}°C\n"
            temp_water = f"Температура воды: {data['response']['temperature']['water']['C']}°C\n"
            description = f"{data['response']['description']['full']}\n"
            gm = data['response']['gm']
            if gm in gm_description_geomagnetic_pattern:
                gm_desc = f"Геомагнитный индекс: {gm} {gm_description_geomagnetic_pattern[gm]}\n"
            else:
                gm_desc = f"Геомагнитный индекс: {gm} (Не удалось получить описание геомагнитных бурь)...\n"
            pressure = f"Атмосферное давление: {data['response']['pressure']['mm_hg_atm']} мм.рт.ст\n"
            humidity = f"Влажность: {data['response']['humidity']['percent']}%\n"
            storm = f"{data['response']['storm']}\n"
            storm_format = "Вероятность грозы: Да\n" if storm == True else "Вероятность грозы: Нет\n"
            precipitation_type = f"{data['response']['precipitation']['type']}\n"
            service_name = '<i>По данным GisMeteo</i>\n'
            if precipitation_type in gm_precipitation_type_pattern:
                pt = gm_precipitation_type_pattern[precipitation_type]
            else:
                pt = "Описание: Посмотри в окно, я не понимаю, что там за погода...\n"
            return f'{date}{emoji_temp}{temp_air}{temp_comfort}{temp_water}{description}{gm_desc}{pressure}{humidity}{storm_format}{pt}{service_name}'
        except Exception as e:
            return f"{str(e)} -- {e}"
    else:
        return f"{response.status_code}"


async def get_weather_gm_city_id_n_d(city_id):
    response = await gm_request_url_forecast(city_id)
    status_code = response.status_code
    if status_code == 200:
        try:
            result = []
            data = response.json()
            service_name = '<i>По данным GisMeteo</i>\n'
            for i in range(6):
                date = f'Дата прогноза: {data["response"][i]["date"]["local"]}\n'
                result.append(date)
                emoji_temp = f'Сведения о температуре: \n'
                result.append(emoji_temp)
                temp_air = f"Температура воздуха: {data['response'][i]['temperature']['air']['C']}°C\n"
                result.append(temp_air)
                temp_comfort = f"Температура по ощущению: {data['response'][i]['temperature']['comfort']['C']}°C\n"
                result.append(temp_comfort)
                temp_water = f"Температура воды: {data['response'][i]['temperature']['water']['C']}°C\n\n"
                result.append(temp_water)
                if i == 5:
                    result.append(service_name)
            return ''.join(result)
        except Exception as e:
            return f"{str(e)} -- {e}"
    else:
        return f"{response.status_code}"


async def main():
    print(await get_weather_gm_city_id('4368'))

if __name__ == '__main__':
    asyncio.run(main())
