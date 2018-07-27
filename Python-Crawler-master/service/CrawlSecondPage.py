import requests
import re
from bs4 import BeautifulSoup
from dao.CRUD import *

index_url = 'http://www.ygdy8.com/index.html'
main_url = 'http://www.ygdy8.com'

#获取次页的html
def get_one_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    r = response.text
    # ignore忽略非gb2312编码的字符
    content = r.encode('ISO-8859-1').decode(response.apparent_encoding, 'ignore')
    return content

#解析html，获取需要的url和name
def parse_one_page(html):
    # 用BeautifulSoup解析数据  python3 必须传入参数二'html.parser' 得到一个对象，接下来获取对象的相关属性
    html = BeautifulSoup(html, 'html.parser')
    uri_name_map = {}
    #获取a标签里所有class=ulink的对象
    for k in html.find_all('a', 'ulink'):
        #过滤无效的key和无效的分类
        if (k.string == None) | (k['href'] == '#'):
            continue
        patt = '^html'
        pattResult = re.match(patt, k['href'])
        if pattResult is not None:
            uri_name_map['/'+k['href']] = k.string
            continue
        uri_name_map[k['href']] = k.string
    return uri_name_map

#插入二级网址,名字,typeCode
def insertDBUrlAndName(map , typeCode):
    dbcrud = CRUD()
    for key in map:
        insert_sql = "INSERT INTO second_url_film_name (second_url , film_name, type_code ) VALUES ( '" + main_url + key + "', '" + map[key] + "', "+ str(typeCode) +");"
        print(insert_sql)
        dbcrud.insert(insert_sql)

#查询
def selectDBBySql(sql):
    dbcrud = CRUD()
    selectResult = dbcrud.select(sql)
    return selectResult

#查询和打印
def selectDBAndPrint():
    dbcrud = CRUD()
    selectSql = 'select * from second_url_film_name'
    selectResult = dbcrud.select(selectSql)
    #打印查询结果
    printSelectResult(selectResult)
    return selectResult

#pring select result
def printSelectResult(data):
    for d in data:
        #注意int类型需要使用str函数转义
        print("ID: " + str(d[0]) + ';  二级地址： ' + d[1] + ";  电源名称： " + d[2] + "; 电影类型code：" + str(d[3]))
#         + "; 电影类型code：" + str(d[3],"") + "; 下载地址：" + d[4]


def main():
    url = 'http://www.ygdy8.com/html/gndy/dyzz/index.html'
    #从数据库获取要访问的二级地址
    sql = 'select * from first_url_type where type_code = 1 '
    selectResult = selectDBBySql(sql)
    # print(selectResult)
    for data in selectResult:
        secondUrl = data[1]
        typeCode = data[3]

    # 获取单页的html
    html = get_one_page(secondUrl)
    uri_name_map = parse_one_page(html)
    # print(uri_name_map)
    insertDBUrlAndName(uri_name_map, typeCode)
    # selectDBAndPrint()

main()