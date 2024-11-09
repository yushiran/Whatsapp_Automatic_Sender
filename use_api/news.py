import requests

def get_top_headlines(api_key, sources='bbc-news'):
    url = f'https://newsapi.org/v2/top-headlines?sources={sources}&apiKey={api_key}'
    response = requests.get(url)
    
    # 检查请求是否成功
    if response.status_code == 200:
        data = response.json()  # 解析 JSON 响应
        articles = data['articles']
        
        result = []
        for i, article in enumerate(articles[:3]):  # 获取前三条新闻
            title = article['title']
            description = article['description']
            url = article['url']
            
            # 添加iOS表情符号并构建每条新闻的信息
            news_info = f"📰 Title: {title}\n💬 Description: {description}\n🔗 URL: {url}\n"
            result.append(news_info)
        
        return result  # 返回包含每条新闻信息的数组
    else:
        return [f'⚠️ Error: {response.status_code}, {response.text}']  # 返回错误信息的数组



# # 使用你的 API 密钥替换 'YOUR_API_KEY'
# api_key = 'YOUR_API_KEY'
# headlines = get_top_headlines('2566660f024c4699834b34f07cbfaf90')
# print(headlines)
