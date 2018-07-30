import sys

import requests
import re
from bs4 import BeautifulSoup
from dao.CRUD import *
import random
from random import choice
import time
import socket
import datetime


index_url = 'http://www.ygdy8.com/index.html'
main_url = 'http://www.ygdy8.com'

# 用于模拟http头的User-agent,随机选择
ua_list = [
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.6; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Mozilla/5.0 (Windows NT 6.1; rv2.0.1) Gecko/20100101 Firefox/4.0.1",
    "Opera/9.80 (Macintosh; Intel Mac OS X 10.6.8; U; en) Presto/2.8.131 Version/11.11",
    "Opera/9.80 (Windows NT 6.1; U; en) Presto/2.8.131 Version/11.11",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_7_0) AppleWebKit/535.11 (KHTML, like Gecko) Chrome/17.0.963.56 Safari/535.11",
    'Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.87 Safari/537.36'
]
# 设置 user-agent列表，每次请求时，可在此列表中随机挑选一个user-agnet
uas = [
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:17.0; Baiduspider-ads) Gecko/17.0 Firefox/17.0",
    "Mozilla/5.0 (Windows; U; Windows NT 5.1; zh-CN; rv:1.9b4) Gecko/2008030317 Firefox/3.0b4",
    "Mozilla/5.0 (Windows; U; MSIE 6.0; Windows NT 5.1; SV1; .NET CLR 2.0.50727; BIDUBrowser 7.6)",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; Trident/7.0; rv:11.0) like Gecko",
    "Mozilla/5.0 (Windows NT 6.3; WOW64; rv:46.0) Gecko/20100101 Firefox/46.0",
    "Mozilla/5.0 (Windows NT 6.3; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/45.0.2454.99 Safari/537.36",
    "Mozilla/5.0 (Windows NT 6.3; Win64; x64; Trident/7.0; Touch; LCJB; rv:11.0) like Gecko",
]




def get_ip():
    """获取代理IP"""
    url = "http://www.xicidaili.com/nn"
    headers = { "Accept":"text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding":"gzip, deflate, sdch",
                "Accept-Language":"zh-CN,zh;q=0.8,en;q=0.6",
                "Referer":"http://www.xicidaili.com",
                "User-Agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.90 Safari/537.36"
                }
    r = requests.get(url,headers=headers)
    soup = BeautifulSoup(r.text, 'html.parser')
    data = soup.table.find_all("td")
    ip_compile= re.compile(r'<td>(\d+\.\d+\.\d+\.\d+)</td>')    # 匹配IP
    port_compile = re.compile(r'<td>(\d+)</td>')                # 匹配端口
    ip = re.findall(ip_compile,str(data))       # 获取所有IP
    port = re.findall(port_compile,str(data))   # 获取所有端口
    return [":".join(i) for i in zip(ip,port)]  # 组合IP+端口，如：115.112.88.23:8080

#获取次页的html
def get_one_page(url, ips=[]):
    get_one_page_start_time = datetime.datetime.now()
    print('连接网址开始：' + url)
    #变化ip进行访问
    # ips = get_ip()
    # ip = random.choice(ips)
    # proxies = {
    #     "http": ip, #"61.135.217.7:80"
    # }
    # print('ip: ' + ip)
    user_agent = random.choice(ua_list)
    headers = {'Accept': '*/*',
               'Origin': 'http://www.ygdy8.com',
               # 'Referer': url,
               "Accept": "text/html,application/xhtml+xml,application/xml;",
               "Accept-Encoding": "gzip, deflate, sdch",
               "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
               'Cache-Control': 'no-cache',
               'User-Agent': user_agent,
               'Connection': 'keep-alive=false',
               }
    headers2 = {"Accept": "text/html,application/xhtml+xml,application/xml;",
                "Accept-Encoding": "gzip, deflate, sdch",
                "Accept-Language": "zh-CN,zh;q=0.8,en;q=0.6",
                "Referer": "",
                "User-Agent": choice(uas),
                }
    global response
    try:
        requests_get_start_time = datetime.datetime.now()
        response = requests.get(url, headers=headers)#timeout=3000,  , proxies=proxies代理变换ip
        requests_get_end_time = datetime.datetime.now()
        print('requests_get funtion used time/microseconds: ', end='')
        print((requests_get_end_time - requests_get_start_time).microseconds / 1000)
    except requests.exceptions.ConnectionError:
        print("ConnectionError")
        # if not ips:
        #     print("not ip")
        #     print(ips)
        #     sys.exit()
        # 删除不可用的代理IP
        # if ip in ips:
        #     print('remove ip: ' + ip)
        #     ips.remove(ip)
        # 重新请求URL
        time.sleep(1)
        get_one_page(url, ips)
    if response.status_code != 200:
        print('访问网站失败，status_code:' + response.status_code + '; 网址为：' + url)
        return None
    print('连接网址成功: ' + url)
    r = response.text
    # print(r)
    # ignore忽略非gb2312编码的字符
    if response.apparent_encoding != 'gb2312':
        content = response.content.decode("gb2312", errors='ignore')
    else:
        content = r.encode('ISO-8859-1').decode(response.apparent_encoding, 'ignore')
    response.close()
    # time.sleep(2)
    get_one_page_end_time = datetime.datetime.now()
    print('get_one_page funtion used time/microseconds: ', end='')
    print((get_one_page_end_time - get_one_page_start_time).microseconds/1000)
    return content

#解析html，获取需要的url和name
def parse_one_page(html):
    parse_one_page_start_time = datetime.datetime.now()
    # 用BeautifulSoup解析数据  python3 必须传入参数二'html.parser' 得到一个对象，接下来获取对象的相关属性
    html = BeautifulSoup(html, 'html.parser')
    labelOfAs = html.find_all('a')
    if labelOfAs is None:
        print('获取下载地址为空,return None')
        return None
    # print('labelOfAs:')
    # print(labelOfAs)
    for labelOfA in labelOfAs:
        # print("labelOfA['href']:")
        # print(labelOfA['href'])
        patt = '(^ftp.*\.mkv$)|(^ftp.*\.mp4$)|(^ftp.*\.rmvb)'
        # print(type(labelOfA.string))
        global pattResult
        try:
            pattResult = re.search(patt, labelOfA['href'])  #labelOfA['href']
        except Exception:
            print('获取href属性失败，执行continue')
            continue

        if pattResult is not None:
            print('获取下载地址成功')
            # print(pattResult.group())
            parse_one_page_end_time = datetime.datetime.now()
            print('parse_one_page funtion used time/microseconds: ', end='')
            print((parse_one_page_end_time - parse_one_page_start_time).microseconds / 1000)
            return pattResult.group()


#查询
def selectDBBySql(sql):
    dbcrud = CRUD()
    selectResult = dbcrud.select(sql)
    return selectResult

#修改下载地址
def updateDBById(downloadUrl, id):
    dbcrud = CRUD()
    sql = "update second_url_film_name set download_ftp_url = '" + downloadUrl +"' where id = " + str(id)+";"
    print("update sql: ")
    print('            ' + sql)
    dbcrud.operateDB(sql)

def get_download_url(singleData):
    starttimeAll = datetime.datetime.now()
    id = singleData[0]
    secondUrl = singleData[1]

    print('==============================  id:' + str(id) + '  ===========================================')
    # 获取单页的html
    ips = []
    html = get_one_page(secondUrl, ips)
    singleDownloadUrl = parse_one_page(html)
    # print(parseResult)
    if singleDownloadUrl is not None:
        print('download url: ')
        print('              ' + singleDownloadUrl)
        updateDBById(singleDownloadUrl, id)
    endtimeAll = datetime.datetime.now()
    print('总耗时/毫秒：', end="")  # end="" 不换行
    print((endtimeAll - starttimeAll).microseconds / 1000)

def get_all_second_level_url():
    # 从数据库获取所有要访问的二级地址
    sql = 'select * from second_url_film_name where id >= 14080;'
    selectResult = selectDBBySql(sql)
    if selectResult is None:
        print("查询所有二级网址失败")
        return None
    return selectResult
    # print(selectResult)

def main():
    # url = 'http://www.ygdy8.com/html/gndy/dyzz/index.html'

    all_second_level_urls = get_all_second_level_url()
    if all_second_level_urls is None:
        return

    for singleSecondUrl in all_second_level_urls:
        get_download_url(singleSecondUrl)

if __name__ == '__main__':
    main()