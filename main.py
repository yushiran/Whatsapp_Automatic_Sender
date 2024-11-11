from __future__ import print_function
from flask import Flask, jsonify
from apscheduler.schedulers.background import BackgroundScheduler
import requests
import schedule
import time
import os
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
    lines = file.readlines()  # Read all lines from the file
    account_sid = lines[0].strip()  # Line 1: Twilio Account SID https://console.twilio.com/
    auth_token = lines[1].strip()  # Line 2: Twilio Authentication Token
    to_whatsapp_number_secure = lines[2].strip()  # Line 3: Secure WhatsApp recipient number
    weatherapi_key = lines[3].strip()  # Line 4: Weather API key https://www.weatherapi.com/my/
    exchange_rate_key = lines[4].strip()  # Line 5: Exchange rate API key https://app.exchangerate-api.com/dashboard/confirmed
    news_api_key = lines[5].strip()  # Line 6: News API key https://newsapi.org/account
    gpt_api_key = lines[6].strip()  # Line 7: GPT API key https://platform.openai.com/api-keys

app = Flask(__name__)
# 本地文件路径，用于存储最新的消息
MESSAGE_FILE = "latest_message.txt"

# client = Client(account_sid, auth_token)
# from_whatsapp_number = 'whatsapp:+14155238886'  # Twilio 提供的 WhatsApp 沙盒号码
# to_whatsapp_number = 'whatsapp:' + to_whatsapp_number_secure   # 收件人的 WhatsApp 号码

# 定义消息更新函数
def update_daily_message():
    # 获取天气、汇率和新闻数据
    weather_response = get_weather_advice('Manchester', weatherapi_key)
    exchange_rate_response = get_exchange_rate(exchange_rate_key)
    news_message = get_top_headlines(news_api_key)
    news_message_str = " ".join(news_message)
    finish_message = generate_gpt_summary(weather_response, news_message_str, gpt_api_key)
    # 构造完整消息内容，遍历news_message数组并加入到字符串中
    message = f"☀️早上好京京!今天是英国时间{datetime.now()}\n{weather_response}\n{exchange_rate_response}\n今天吃早饭的时候可以看看这些新闻哦：\n"
    for news in news_message:
        message += f"- {news}\n"
    message += finish_message  # 添加总结内容
    # 将消息保存到本地文件
    with open(MESSAGE_FILE, "w", encoding="utf-8") as file:
        file.write(message)
    print(f"Message updated and saved at {datetime.now()}")

# 检查文件是否存在，如果不存在则立即更新
if not os.path.exists(MESSAGE_FILE):
    print("Message file not found. Updating message for the first time.")
    update_daily_message()

# API端点：读取并返回最新的消息
@app.route('/get_text', methods=['GET'])
def get_text():
    if os.path.exists(MESSAGE_FILE):
        with open(MESSAGE_FILE, "r", encoding="utf-8") as file:
            message = file.read()
    else:
        message = "暂无消息，请稍后再试。"
    return jsonify({"message": message})

# 使用APScheduler，每天早上7:30更新一次消息
scheduler = BackgroundScheduler()
scheduler.add_job(func=update_daily_message, trigger="cron", hour=6, minute=30)
scheduler.start()

# 主程序
if __name__ == '__main__':
    try:
        app.run(host='0.0.0.0', port=5000)
    except (KeyboardInterrupt, SystemExit):
        scheduler.shutdown()