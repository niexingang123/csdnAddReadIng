import re
import requests
from requests import RequestException
import time
import random
from fake_useragent import UserAgent
from bs4 import BeautifulSoup
import threading

urls = [
            'https://blog.csdn.net/Z1591090/article/details/82743872',
            'https://blog.csdn.net/Z1591090/article/details/88355955',
            'https://blog.csdn.net/Z1591090/article/details/82772176',
            'https://blog.csdn.net/Z1591090/article/details/88066034',
            'https://blog.csdn.net/Z1591090/article/details/81170760',
            'https://blog.csdn.net/Z1591090/article/details/88656284',
            'https://blog.csdn.net/Z1591090/article/details/52839715',
            'https://blog.csdn.net/Z1591090/article/details/88819109',
            'https://blog.csdn.net/Z1591090/article/details/52848654',
            'https://blog.csdn.net/Z1591090/article/details/68942656',
            'https://blog.csdn.net/Z1591090/article/details/82737187',
            'https://blog.csdn.net/Z1591090/article/details/88314021',
            'https://blog.csdn.net/Z1591090/article/details/81286578',
            'https://blog.csdn.net/Z1591090/article/details/88344066',
            'https://blog.csdn.net/Z1591090/article/details/89337802',
            'https://blog.csdn.net/Z1591090/article/details/88644953',
            'https://blog.csdn.net/Z1591090/article/details/82787716',
            'https://blog.csdn.net/Z1591090/article/details/86545917',
            'https://blog.csdn.net/Z1591090/article/details/89400543',
            'https://blog.csdn.net/Z1591090/article/details/91416199',
            'https://blog.csdn.net/Z1591090/article/details/88669762',
            'https://blog.csdn.net/Z1591090/article/details/88819505',
            'https://blog.csdn.net/Z1591090/article/details/81240875',
            'https://blog.csdn.net/Z1591090/article/details/88366916',
            'https://blog.csdn.net/Z1591090/article/details/83311254',
            'https://blog.csdn.net/Z1591090/article/details/95967819',
            'https://blog.csdn.net/Z1591090/article/details/90705089',
            'https://blog.csdn.net/Z1591090/article/details/81180115',
            'https://blog.csdn.net/Z1591090/article/details/101695441',
            'https://blog.csdn.net/Z1591090/article/details/103090243'
        ]

def get_proxy():
    try:
        r = requests.get('http://127.0.0.1:5000/get')
        proxy = BeautifulSoup(r.text, "lxml").get_text()
        if proxy=="null":
            return None
        return proxy
    except:
        print("获取代理异常")
        return None

def get_page(url):
    try:
        ua = UserAgent(verify_ssl=False)
        headers = {
            'Referer': 'https://blog.csdn.net',  # 伪装成从CSDN博客搜索到的文章
            'User-Agent': ua.random
        }
        proxy = None#get_proxy()
        if proxy :
            proxies = {'https': proxy}
        else:
            proxies=None
        response = requests.get(url, headers=headers, proxies=proxies)
        if response.status_code == 200:
            return response.text
        return None
    except RequestException:
        print('请求出错')
        return None


def parse_page(html):
    try:
        read_num = int(re.compile('<span.*?read-count.*?(\d+).*?</span>').search(html).group(1))
        return read_num
    except Exception:
        print('解析出错')
        return None


def main(url):
    try:
        while 1:
            html = get_page(url)
            if html:
                read_num = parse_page(html)
                if read_num:
                    print(url,'当前阅读量：', read_num)
            sleep_time = random.randint(60, 70)
            print('please wait', sleep_time, 's')
            time.sleep(sleep_time)  # 设置访问频率，过于频繁的访问会触发反爬虫
    except Exception:
        print('出错啦！')


if __name__ == '__main__':
    for url in urls:
        td = threading.Thread(target=main, args=(url,))
        td.start()