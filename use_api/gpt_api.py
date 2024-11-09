import requests

from openai import OpenAI

def generate_gpt_summary(weather, news_info, openai_key):
    client = OpenAI(
    # This is the default and can be omitted
    api_key=openai_key,
    )
    """调用 GPT API 生成总结或祝福"""
    prompt = f"""
    Weather: {weather}
    News Highlights: {news_info}

    请结合今天的天气和新闻给京京一个今天的鼓励和祝福，最好能够引用名人名言或者名著（如果引用请标明出处），字数在六十字以内。
    """

    chat_completion = client.chat.completions.create(
    messages=[
        {
            "role": "user",
            "content": prompt,
        }
    ],
    model="gpt-3.5-turbo",
    )
    
    return f"🧸{chat_completion.choices[0].message.content}"