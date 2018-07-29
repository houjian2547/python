
import requests
import re
from bs4 import BeautifulSoup
from dao.CRUD import *

'''
    抓取电源天堂首页网址和分类名字
'''

index_url = 'http://www.ygdy8.com/index.html'
main_url = 'http://www.ygdy8.com'

#获取主页的html
def get_one_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    contentType = response.headers['content-type']
    # print('contentType为:'+contentType)
    encoding = response.encoding
    # print("encoding结果编码为:"+encoding)
    # print('apparent_encoding源编码为:'+response.apparent_encoding)
    r = response.text
    # ignore忽略非gb2312编码的字符
    content = r.encode('ISO-8859-1').decode(response.apparent_encoding, 'ignore')
    return content

#解析html，获取需要的url和name
def parse_one_page(html):
    # 用BeautifulSoup解析数据  python3 必须传入参数二'html.parser' 得到一个对象，接下来获取对象的相关属性
    html = BeautifulSoup(html, 'html.parser')
    # 读取title内容
    # print(html.title)
    # 读取body
    bodyString = html.body
    # print(bodyString)
    # print(bodyString.select('div #menu ul li a'))
    # print('-----------------------------')
    uri_name_map = {}
    for k in bodyString.find_all('a'):
        # print(k)
        #过滤无效的key和无效的分类
        if (k.string == None) | (k['href'] == '#'):
            continue
        patt = '^html'
        pattResult = re.match(patt, k['href'])
        if pattResult is not None:
            uri_name_map['/'+k['href']] = k.string
            continue
        uri_name_map[k['href']] = k.string
        # print(k['href'])  # 查a标签的href值
        # print(k.string)  # 查a标签的string
    #过滤安卓软件下载
    uri_name_map.pop('http://m.dytt8.net/dytt8.apk')
    #过滤游戏下载
    uri_name_map.pop('/html/game/index.html')
    #过滤不一样的页面
    uri_name_map.pop('/html/gndy/index.html')
    # print(uri_name_map)
    return uri_name_map

#插入主页里的分类网址和分类名字
def insertUrlTypename(urlTypeMap):
    dbcrud = CRUD()
    # dbcrud.select()
    i = 1
    for key in urlTypeMap:
        insert_sql = "INSERT INTO first_url_type(url , type_name, type_code ) VALUES ( '" + main_url + key + "', '" + urlTypeMap[key] + "',"  + str(i) + ")"
        print(insert_sql)
        dbcrud.insert(insert_sql)
        i += 1

#查询结果
def selectAndPrint():
    dbcrud = CRUD()
    selectSql = 'select * from first_url_type'
    selectResult = dbcrud.select(selectSql)
    #打印查询结果
    printSelectResult(selectResult)
    return selectResult

#pring select result
def printSelectResult(data):
    for d in data:
        #注意int类型需要使用str函数转义
        print("ID: " + str(d[0]) + '; url： ' + d[1] + "; 电源分类： " + d[2] + "; 电影类型code：" + str(d[3]))

def deleteAllTableDate():
    dbcrud = CRUD()
    sql = 'delete from first_url_type'
    dbcrud.deleteAllTableDate(sql)

#主方法
def main():
    #获取单页的html
    html = get_one_page(index_url)

    #解析html，获取url type 的map
    urlTypeMap = parse_one_page(html)

    #插入mysql
    # deleteAllTableDate()
    insertUrlTypename(urlTypeMap)

    #查询插入的结果
    selectAndPrint()

'''
运行程序
'''
if __name__ == '__main__':
    main()