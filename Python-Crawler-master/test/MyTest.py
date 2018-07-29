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
    # print(r)
    if response.apparent_encoding != 'gb2312':
        html = response.content.decode("gb2312", errors='ignore')

    print(response.apparent_encoding)
    # print(requests.utils.get_encodings_from_content(response.text))
    # ignore忽略非gb2312编码的字符
    # result = response.content.decode('GB2312')

    html = response.content.decode("gb2312", errors='ignore')
    # print(html)
    # content = r.encode('GB2312').decode('GB2312', 'ignore')
    # return content

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


#获取所有的二级网页列表
def getAllSecondUrl(firstPageUrl):
    html = get_one_page(firstPageUrl)
    dom = BeautifulSoup(html, 'html.parser')
    content = dom.find_all('option', value = re.compile('list_'))
    lastPageNo = len(content)
    optionTag = content[lastPageNo - 1]
    # print(type(optionTag))
    # print(optionTag.name)
    # print(optionTag.attrs['value'])
    valueString = optionTag.attrs['value']
    patt = '_\w*_'
    regResult = re.search(patt, valueString)
    urlMap = {}
    if regResult is not None:
        # print(regResult.group())
        urlMap['_preUrl_'] = regResult.group()
        urlMap['lastPageNo'] = lastPageNo
        return urlMap

def main():
    downLoadUrl = 'http://www.ygdy8.com/html/gndy/dyzz/list_23_3.html'
    # 获取单页的html
    html = get_one_page(downLoadUrl)
    uri_name_map = parse_one_page(html)
    print(uri_name_map)

# main()

url1 = 'http://www.ygdy8.com/html/gndy/china/index.html'
patt = '/\w*/index.html'
pattResult = re.search(patt, url1).group()
patt = '/\w*/'
pattResult = re.search(patt, pattResult).group()
# print(pattResult)

#/html/gndy/jddy/20180606/56974.html
#/html/gndy/dyzz/index.html
str = '/html/gndy/dyzz/index.html'
patt = 'index'
pattResult = re.search(patt, str)
# if pattResult is not None:
#    print(111111)

#      http://www.ygdy8.com/html/tv/hytv/index.html
#      http://www.ygdy8.com/html/dongman/index.html
#      http://www.ygdy8.com/html/gndy/jddy/20160320/50541.html
str = 'http://www.ygdy8.com/html/gndy/dyzz/index.html'
print(str.split('/'))
