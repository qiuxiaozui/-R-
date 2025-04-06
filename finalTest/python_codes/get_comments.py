import asyncio
import aiohttp
from bs4 import BeautifulSoup
from python_codes.get_cookie import CookieGenerator

async def get_comment(stock_id, stock_name, page):
    generator = CookieGenerator(stock_id, stock_name)
    cookies = generator.generate_cookie()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'priority': 'u=0, i',
        'referer': f'https://guba.sina.com.cn/?s=bar&name={stock_id}&type=0&page={page}',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'document',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-user': '?1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    }

    params = {
        's': 'bar',
        'name': stock_id,
        'type': '0',
        'page': page,
    }

    async with aiohttp.ClientSession() as session:
        async with session.get('https://guba.sina.com.cn/', params=params, cookies=cookies, headers=headers) as response:
            return await response.text()

async def fetch_url(data, url_list):
    soup = BeautifulSoup(data, 'html.parser')
    links = soup.find_all(
        'a',
        target="_blank",
        class_="linkblack f14"
    )
    for link in links:
        new_link = "https://guba.sina.com.cn/" + link.get('href')
        if new_link and new_link not in url_list:  # 确保链接有效且未重复
            url_list.append(new_link)

async def main():
    url_list = []
    stock_id = "sz002594"
    stock_name = "比亚迪"

    for page in range(1, 50):
        data = await get_comment(stock_id, stock_name, page)
        await fetch_url(data, url_list)

    print(url_list)

if __name__ == '__main__':
    asyncio.run(main())