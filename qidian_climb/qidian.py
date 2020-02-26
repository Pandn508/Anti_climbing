import requests
import re
from lxml import etree
import json
import time
import os

def get_one_book(url):
    try:
        header = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/79.0.3945.88 Safari/537.36'
        }
        responce = requests.get(url, headers=header)
        responce.encoding = responce.apparent_encoding
        if responce.status_code == 200:
            return responce.text
        return None
    except requests.RequestException:
        return None

#书目录链接0与书名1
def re_book_url(html_main):
    html = etree.HTML(html_main)
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))
    books_url = html.xpath('//div[@class="book-img-box"]/a/@href')
    books_name = html.xpath('//div[@class="book-mid-info"]/h4/a/text()')
    for info in zip(books_url,books_name):
        yield info

# 目录名0，内容url1
def re_catalog_name(html_book):
    html = etree.HTML(html_book)
    # result = etree.tostring(html)
    # print(result.decode('utf-8'))
    books_catalog = html.xpath('//div[@class="volume-wrap"]//ul[@class="cf"]/li/a/text()')
    books_catalog_url = html.xpath('//div[@class="volume-wrap"]//ul[@class="cf"]/li/a/@href')
    # print(books_catalog_url)
    for info in zip(books_catalog, books_catalog_url):
        yield info
#内容
def re_story(html_ca):
    html = etree.HTML(html_ca)
    story = html.xpath('//div[@class="read-content j_readContent"]/p//text()')
    # print(story)
    yield story

def main(page):
    url_main = 'https://www.qidian.com/free/all?orderId=&vip=hidden&style=1&pageSize=20&siteid=1&pubflag=0&hiddenField=1&page='+str(page)
    html_main = get_one_book(url_main)
    # print(type(html_main))
# 数目路连接
    for book_url in re_book_url(html_main):
        html_book = get_one_book('https:' + book_url[0] + '#Catalog')
        # print(html_book)
# 目录和内容
        for catalog in re_catalog_name(html_book):
            print(catalog)
            html_ca = get_one_book('https:' + catalog[1])
            # print(html_ca)

            for story in re_story(html_ca):
                result = '\n'.join(story)
                print(result)
                root = 'D://pachong//qidian//'
                link = root + book_url[1]
                if not os.path.exists(link):
                    os.makedirs(link)
                all_link = link + '//' + catalog[0] + '.txt'
                print(all_link)
                with open(all_link, 'a', encoding='utf-8') as f:
                    f.write(result)
                    f.close()

if __name__ == '__main__':
    for i in range(1, 5):
        main(page=i)
        time.sleep(5)