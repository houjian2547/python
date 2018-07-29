import requests
import re
from bs4 import BeautifulSoup
from dao.CRUD import *

index_url = 'http://www.ygdy8.com/index.html'
main_url = 'http://www.ygdy8.com'
#http://www.ygdy8.com/html/tv/hytv/index.html

#获取次页的html
def get_one_page(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    r = response.text
    # ignore忽略非gb2312编码的字符
    if response.apparent_encoding != 'gb2312':
        content = response.content.decode("gb2312", errors='ignore')
    else:
        content = r.encode('ISO-8859-1').decode(response.apparent_encoding, 'ignore')
    return content

#解析html，获取需要的url和name
def parse_one_page(html):
    # 用BeautifulSoup解析数据  python3 必须传入参数二'html.parser' 得到一个对象，接下来获取对象的相关属性
    html = BeautifulSoup(html, 'html.parser')
    uri_name_map = {}
    #获取a标签里所有class=ulink的对象
    # print(html.find_all('a', 'ulink'))
    for k in html.find_all('a', 'ulink'):
        #过滤无效的key和无效的分类
        if (k.string == None) | (k['href'] == '#'):
            continue
        # 过滤没有数字的href
        patt = 'index'
        pattResult = re.search(patt, k['href'])
        if pattResult is not None:
            continue
        #缺少/的添加/
        patt = '^html'
        pattResult = re.match(patt, k['href'])
        if pattResult is not None:
            uri_name_map['/'+k['href']] = k.string
            continue
        uri_name_map[k['href']] = k.string
        # print(uri_name_map)
    return uri_name_map

#插入二级网址,名字,typeCode
def insertDB(map, typeCode):
    dbcrud = CRUD()
    for key in map:
        insert_sql = "INSERT INTO second_url_film_name (second_url , film_name, type_code ) VALUES ( '" + main_url + key + "', '" + map[key] + "', "+ str(typeCode) +");"
        # print(insert_sql)
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
        print("ID:" + str(d[0]) + '; 二级地址： ' + d[1] + "; 电源名称： " + d[2] + "; 电影类型code：" + str(d[3]) + "; 下载地址：" + d[4])

#获取所有的二级网页列表
def getAllSecondUrl(firstPageUrl):
    html = get_one_page(firstPageUrl)
    dom = BeautifulSoup(html, 'html.parser')
    content = dom.find_all('option', value = re.compile('list_'))
    lastPageNo = len(content)
    optionTag = content[lastPageNo - 1]
    print(type(optionTag))
    print(optionTag.name)
    print(optionTag.attrs['value'])
    valueString = optionTag.attrs['value']
    patt = '_\w*_'
    regResult = re.search(patt, valueString)
    urlMap = {}
    if regResult is not None:
        print(regResult.group())
        urlMap['_preUrl_'] = regResult.group()
        urlMap['lastPageNo'] = lastPageNo
        return urlMap

def main():
    #http://www.ygdy8.com/html/gndy/china/list_4_101.html
    # 获取一个分类
    sql = 'select * from first_url_type where id >=86'
    selectResult = selectDBBySql(sql)
    print('获取分类地址成功')
    for data in selectResult:
        secondUrl = data[1]
        typeCode = data[3]
        print('获取所有的url开始')
        map = getAllSecondUrl(secondUrl)
        print('获取所有的url end')
        lastPageNo = map.get('lastPageNo')
        _preUrl_ = map.get('_preUrl_')
        i = 1

        patt = '/\w*/index.html'
        pattResult = re.search(patt, secondUrl).group()
        patt = '/\w*/'
        pattResult = re.search(patt, pattResult).group()

        while i <= lastPageNo:
            # http://www.ygdy8.com/html/gndy/dyzz/list_23_2.html
            # http://www.ygdy8.com/html/tv/hytv/index.html
            downLoadUrl = main_url + '/html/' + pattResult + 'list' + _preUrl_ + str(i) + '.html'
            print("---------------开始下载第" + str(i) + "页/" + str(lastPageNo) + "--------------")
            print(downLoadUrl)
            # 获取单页的html
            html = get_one_page(downLoadUrl)
            uri_name_map = parse_one_page(html)
            print('------------------uri_name_map---------------')
            print(uri_name_map)
            print('循环插入开始')
            insertDB(uri_name_map, typeCode)
            print('循环插入end')
            # selectDBAndPrint()
            i += 1


# typeCode=1 最后一条记录是 http://www.ygdy8.com/html/gndy/dyzz/20100203/24340.html
main()