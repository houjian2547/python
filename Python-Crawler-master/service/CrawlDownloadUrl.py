
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
    labelOfAs = html.find_all('a')
    # print(labelOfAs)
    for labelOfA in labelOfAs:
        # print(labelOfA['href'])
        patt = '(^ftp.*\.mkv$)|(^ftp.*\.mp4$)'
        pattResult = re.search(patt, labelOfA['href'])
        if pattResult is not None:
            print(pattResult.group())
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
    dbcrud.operateDB(sql)


def main():
    url = 'http://www.ygdy8.com/html/gndy/dyzz/index.html'
    #从数据库获取要访问的二级地址
    sql = 'select * from second_url_film_name'
    selectResult = selectDBBySql(sql)
    if selectResult is None:
        print("查询失败")
        return
    # print(selectResult)
    for data in selectResult:
        id = data[0]
        secondUrl = data[1]
        # 获取单页的html
        html = get_one_page(secondUrl)
        singleDownloadUrl = parse_one_page(html)
        # print(parseResult)
        updateDBById(singleDownloadUrl, id)

main()