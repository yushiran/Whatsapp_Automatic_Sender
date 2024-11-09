# -*- coding: utf-8 -*-

from __future__ import print_function
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint


def get_weather_advice(city, api_key):
    # Configure API key authorization
    configuration = weatherapi.Configuration()
    configuration.api_key['key'] = api_key

    # Create an instance of the API class
    api_instance = weatherapi.APIsApi(weatherapi.ApiClient(configuration))
    q = city  # Pass city name as parameter
    days = 1

    try:
        # Get the weather forecast
        api_response = api_instance.forecast_weather(q=q, days=days)
        data = api_response['forecast']['forecastday'][0]['day']

        # 提取数据
        uv_index = data.get('uv', 0)
        rain_chance = data.get('daily_chance_of_rain', 0)
        condition = data['condition']['text']
        avg_temp = data.get('avgtemp_c', 0)

        # 判断是否需要涂防晒
        if uv_index > 3:
            sunscreen_advice = f"🌞 紫外线指数为{uv_index},建议涂防晒"
        else:
            sunscreen_advice = f"🌤 紫外线指数为{uv_index},紫外线较弱，不需要涂防晒"

        # 判断是否需要带伞
        if rain_chance > 0:
            umbrella_advice = f"☔️ 降雨概率为{rain_chance},建议带伞"
        else:
            umbrella_advice = f"☀️ 降雨概率为{rain_chance}，不用带伞"

        # 天气描述
        weather_condition = f"🌦 今天{city}的天气是{condition}"

        # 判断穿什么衣服
        if avg_temp < 5:
            clothing_advice = f'🧥 今天的平均气温是{avg_temp}度,一点要多穿衣服哦'
        elif avg_temp < 10:
            clothing_advice = f"🧥 今天的平均气温是{avg_temp}度,建议穿外套，天气偏冷"
        elif avg_temp < 20:
            clothing_advice = f"👕 今天的平均气温是{avg_temp}度,适合穿长袖或轻便的外套"
        else:
            clothing_advice = f"👕 今天的平均气温是{avg_temp}度,天气较暖，穿轻便衣服即可"

        # 汇总所有建议
        advice = f"{weather_condition}\n{sunscreen_advice}\n{umbrella_advice}\n{clothing_advice}"
        return advice

    except ApiException as e:
        return f"🚨 Exception when calling APIsApi->forecast_weather: {e}"
