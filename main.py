from __future__ import print_function
from twilio.rest import Client
import requests
import schedule
import time
import weatherapi
from weatherapi.rest import ApiException
from pprint import pprint
from datetime import datetime
from use_api.weather import get_weather_advice
from use_api.exchange_rate import get_exchange_rate
from use_api.news import get_top_headlines
from use_api.gpt_api import generate_gpt_summary

# Twilio 帐户 SID 和身份验证令牌
with open('pwd.key', 'r') as file:
    lines = file.readlines()
    account_sid = lines[0].strip()
    auth_token = lines[1].strip()
    to_whatsapp_number_secure = lines[2].strip()
    weatherapi_key = lines[3].strip()
    exchange_rate_key = lines[4].strip()
    news_api_key = lines[5].strip()
    gpt_api_key = lines[6].strip()

client = Client(account_sid, auth_token)
from_whatsapp_number = 'whatsapp:+14155238886'  # Twilio 提供的 WhatsApp 沙盒号码
to_whatsapp_number = 'whatsapp:' + to_whatsapp_number_secure   # 收件人的 WhatsApp 号码

def send_daily_message():
    # 获取天气数据
    weather_response = get_weather_advice('Manchester', weatherapi_key)

    # 获取汇率数据
    exchange_rate_response = get_exchange_rate(exchange_rate_key)

    # 获取新闻数据
    news_message = get_top_headlines(news_api_key)

    # 构造消息
    message = f"☀️早上好京京!\n{weather_response}\n{exchange_rate_response}\n今天吃早饭的时候可以看看这些新闻哦：\n"

    # 用 OpenAI 来总结一下
    news_message_str = " ".join(news_message)
    finish_message = generate_gpt_summary(weather_response, news_message_str, gpt_api_key)

    # 发送消息
    try:
        client.messages.create(
            body=message,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        time.sleep(1)
        for i in news_message:
            client.messages.create(
                body=i,
                from_=from_whatsapp_number,
                to=to_whatsapp_number
            )
            time.sleep(1)
        client.messages.create(
            body=finish_message,
            from_=from_whatsapp_number,
            to=to_whatsapp_number
        )
        time.sleep(1)
        print("Message sent successfully!")
    except Exception as e:
        print(f"Error sending message: {e}")

# 设置定时任务，每天早上6点半执行
schedule.every().day.at("06:30").do(send_daily_message)

def main():
    while True:
        schedule.run_pending()
        # send_daily_message()
        # 获取今天的日期
        today = datetime.today().date()
        print(f'Jingjing Whatsapp Structure is working!Today is {today}\n')
        time.sleep(1)

if __name__ == '__main__':
    main()
