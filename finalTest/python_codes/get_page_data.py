import requests
from bs4 import BeautifulSoup
from python_codes.get_cookie import CookieGenerator
stock_id = "sz002594"
stock_name = "比亚迪"
generator = CookieGenerator(stock_id, stock_name)
cookies = generator.generate_cookie()

headers = {
    'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
    'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
    'cache-control': 'max-age=0',
    'priority': 'u=0, i',
    'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
    'sec-ch-ua-mobile': '?0',
    'sec-ch-ua-platform': '"Windows"',
    'sec-fetch-dest': 'document',
    'sec-fetch-mode': 'navigate',
    'sec-fetch-site': 'none',
    'sec-fetch-user': '?1',
    'upgrade-insecure-requests': '1',
    'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
}


response = requests.get('https://guba.sina.com.cn//?s=thread&tid=720454&bid=10199', cookies=cookies, headers=headers)
data = response.text
#<div class='ilt_p' id="thread_content">
soup = BeautifulSoup(data, 'html.parser')
links = soup.find_all(
    'div',
    id="thread_content",
    class_='ilt_p'
)
article_list = []
for link in links:
    article_list.append(link.get_text())