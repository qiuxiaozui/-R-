from python_codes.check_id import get_stock_code, get_stock_name
from python_codes.get_cookie import CookieGenerator
import requests
import rpy2.robjects as ro
import os
import asyncio
import aiohttp
from bs4 import BeautifulSoup
import json

# 异步获取评论链接模块
async def get_comment(stock_id, stock_name, page):
    generator = CookieGenerator(stock_id, stock_name)
    cookies = generator.generate()
    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    }

    async with aiohttp.ClientSession() as session:
        async with session.get(
                url='https://guba.sina.com.cn/',
                params={'s': 'bar', 'name': stock_id, 'type': '0', 'page': page},
                cookies=cookies,
                headers=headers
        ) as response:
            return await response.text()


async def fetch_comments(stock_id, stock_name, max_pages=5):
    url_list = []
    tasks = [get_comment(stock_id, stock_name, page) for page in range(1, max_pages + 1)]

    for future in asyncio.as_completed(tasks):
        data = await future
        soup = BeautifulSoup(data, 'html.parser')
        links = soup.select('a[target="_blank"].linkblack.f14')
        for link in links:
            new_link = "https://guba.sina.com.cn/" + link.get('href')
            if new_link not in url_list:
                url_list.append(new_link)
    return url_list

def get_BaseData():
    selection = input("输入股票代码按1，输入股票名称按2：")
    if selection == "1":
        stock_code = input("输入股票代码：")
        return stock_code, get_stock_name(stock_code)
    elif selection == "2":
        try:
            market = input('输入市场（"A": A股, "HK": 港股, "US": 美股）：')
            name = input("输入名称：")
            return get_stock_code(name, market), name
        except:
            print("检查输入并重试")
            get_BaseData()
    else:
        print("无效输入，请重试")
        get_BaseData()
def get_stock_data(stock_id, stock_name, save_dir):
    cookie_generate = CookieGenerator(stock_id, stock_name)
    cookies = cookie_generate.generate()
    headers = {
        'accept': '*/*',
        'accept-language': 'zh-CN,zh;q=0.9,en;q=0.8,en-GB;q=0.7,en-US;q=0.6',
        'referer': f'https://finance.sina.com.cn/realstock/company/{stock_id}/nc.shtml',
        'sec-ch-ua': '"Chromium";v="134", "Not:A-Brand";v="24", "Microsoft Edge";v="134"',
        'sec-ch-ua-mobile': '?0',
        'sec-ch-ua-platform': '"Windows"',
        'sec-fetch-dest': 'script',
        'sec-fetch-mode': 'no-cors',
        'sec-fetch-site': 'same-site',
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0',
    }
    response = requests.get(
        f'https://cn.finance.sina.com.cn/minline/getMinlineData?symbol={
        stock_id}&callback=var%20t1{stock_id}=&version=7.11.0&dpc=1',
        cookies=cookies,
        headers=headers,
    )
    json_data = response.text.replace(f"var t1{stock_id}=(","").replace(")","")
    with open(f'{save_dir}/stock_data.json', 'w', encoding='utf-8') as f:
        f.write(json_data)
        print(f"获取股票数据成功，数据已保存于'{save_dir}/stock_data.json',准备绘图")
# 同步内容提取模块
def get_article_content(url, stock_id, stock_name):
    generator = CookieGenerator(stock_id, stock_name)
    cookies = generator.generate()

    response = requests.get(url, cookies=cookies, headers={
        'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/134.0.0.0 Safari/537.36 Edg/134.0.0.0'
    })

    soup = BeautifulSoup(response.text, 'html.parser')
    content_div = soup.find('div', {'id': 'thread_content', 'class': 'ilt_p'})
    return content_div.get_text(strip=True) if content_div else ''

# 主流程模块
async def full_workflow(stock_id, stock_name, save_dir):
    get_stock_data(stock_id, stock_name, save_dir)
    print("开始抓取评论链接...")
    comment_links = await fetch_comments(stock_id, stock_name)
    print("开始提取文章内容...")
    articles = []
    for link in comment_links:
        content = get_article_content(link, stock_id, stock_name)
        articles.append({'url': link, 'content': content})
    with open(f'{save_dir}/comments.json', 'w', encoding='utf-8') as f:
        json.dump(articles, f, ensure_ascii=False)
    print(f"评论数据已保存至 {save_dir}/comments.json")


if __name__ == '__main__':
    # os.environ['R_HOME'] = 'C:/Program Files/R/R-4.4.3'
    save_path = input("输入保存文件夹路径（默认result）: ") or "result"
    stock_id, stock_name = get_BaseData()
    # 运行异步任务
    loop = asyncio.get_event_loop()
    loop.run_until_complete(full_workflow(stock_id, stock_name, save_path))

    # 生成可视化报表
    ro.r.source("main.R")
    ro.r['create_dashboard'](file_name=save_path)