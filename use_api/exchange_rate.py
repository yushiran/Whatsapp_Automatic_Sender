import requests

def get_exchange_rate(key):
    url = f"https://v6.exchangerate-api.com/v6/{key}/latest/GBP"
    
    # 发送 GET 请求
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        # 如果成功，解析 JSON 数据
        data = response.json()
        answer = f"💱 现在的 GBP -> CNY 汇率为：{data['conversion_rates']['CNY']}。"
        return answer
    else:
        return f"⚠️ Error: Unable to fetch data (Status Code: {response.status_code})"
