import os
import subprocess
import time
from dao.CRUD import *
from common.ThreadUtils import *


# thunder_path = 'D:\\other files\\thunder\\Program\\thunderstart.exe'
# save_path = 'D:\\film'
thunder_path = 'F:\\xunlei\\Program\\thunderstart.exe'
save_path = 'F:\\film'

def download_with_thunder(thunder_url):
    print('启动迅雷开始')
    # subprocess.call([thunder_path, thunder_url])
    os.system(r'"F:\xunlei\Program\thunderstart.exe" {url}'.format(url=thunder_url))
    print('启动迅雷成功')
    time.sleep(40)
    filename = get_filename(thunder_url)
    print("正在下载 {}".format(filename))
    # 检测任务是否已开始
    if check_start(filename):
        print('下载任务启动成功')
        while True:
            # 每分钟检测一次是否下载完成
            time.sleep(60)
            if check_end(filename):
                print('每60s检测一次是否下载完成: 完成 , ' + filename)
                return True
            else:
                print('每60s检测一次是否下载完成: 未完成 , ' + filename)
    else:
        print('下载任务启动失败')
        return False

def check_start(filename):
    '''
    检测文件是否开始下载
    '''
    cache_file = filename+".xltd"
    return os.path.exists(os.path.join(save_path, cache_file))

def check_end(fiename):
    '''
    检测文件是否下载完成
    '''
    return os.path.exists(os.path.join(save_path, fiename))

def get_filename(url):
    return os.path.split(url)[1]

def startDownload(downloadUrl):
    # 开始循环下载
    if downloadUrl is None:
        print('id: ' + str(id) + '下载地址为空')
        return
    print('开始下载id: ' + str(id) + ' 下载地址：', end='')
    print(str(downloadUrl))
    if download_with_thunder(downloadUrl):
        print("======下载完成======", end='')
        print('id: ' + str(id) + '下载地址：', end='')
        print(str(downloadUrl))
    else:
        print("=======下载失败=====")

# 获取要下载的网址集合
def getDownloadUrls():
    selectSql = 'select * from second_url_film_name limit 5;'
    dbcrud = CRUD()
    downloadObjs = dbcrud.select(selectSql)
    return downloadObjs


def main():
    downloadObjs = getDownloadUrls()
    threadNum = len(downloadObjs)
    print('一共启动线程数：' + str(threadNum))
    indexThread = 1
    for downloadObj in downloadObjs:
        # id = downloadObj[0]
        downloadUrl = downloadObj[4]
        print('启动第' + str(indexThread) + '个线程')
        indexThread += 1
        t = MyThread(startDownload, downloadUrl)
        time.sleep(10)
        t.start()

if __name__ == '__main__':
    print("=======电影自动下载程序启动=========")
    main()

    # threads = []
    # threads.append(t)
    # for i in threads:
    #     t.join()


