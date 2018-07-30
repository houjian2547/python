import os
import subprocess
import base64

thunder_path = 'F:\\xunlei\Program\Thunder.exe'


def Url2Thunder(url):
    url = 'AA' + url + 'ZZ'
    url = base64.b64encode(url.encode('ascii'))
    url = b'thunder://' + url
    thunder_url = url.decode()
    return thunder_url


def download_with_thunder(thunder_url):
    # thunder_url = Url2Thunder(file_url)
    subprocess.call([thunder_path, thunder_url])


def download_address_translation(original_address):
    original_address = str(original_address)
    if "thunder://" in original_address:
        original_address = original_address.replace('thunder://', '')
        original_address = base64.b64decode(original_address)
        original_address = original_address.decode('gbk')
        original_address = original_address[2:len(original_address)-2]
    if "flashget://" in original_address:
        original_address = original_address.replace('flashget://', '')
        original_address = original_address.replace('flashget://', '')
        original_address = base64.b64decode(original_address)
        original_address = original_address.decode('gbk')
        original_address = original_address[10:len(original_address) - 10]
    if "qqdl://" in original_address:
        original_address = original_address.replace('qqdl://', '')
        original_address = original_address.replace('qqdl://', '')
        original_address = base64.b64decode(original_address)
        original_address = original_address.decode('gbk')
    temp_address = "AA"  + original_address + "ZZ"
    temp_address = bytes(temp_address, encoding='gbk')
    thunder_address = "thunder://"+base64.b64encode(temp_address).decode('gbk')

    temp_address = "[FLASHGET]"  + original_address  + "[FLASHGET]"
    temp_address = bytes(temp_address, encoding='gbk')
    flashget_address = "flashget://"  + base64.b64encode(temp_address).decode('gbk')

    temp_address = original_address
    temp_address = bytes(temp_address, encoding='gbk')
    qqdl_address = "qqdl://" +  base64.b64encode(temp_address).decode('gbk')

    return {'origin': original_address,'thunder': thunder_address, 'flashget': flashget_address, 'qqdl': qqdl_address }



if __name__ == '__main__':
    url = 'ftp://ygdy8:ygdy8@yg45.dydytt.net:3116/阳光电影www.ygdy8.com.侏罗纪世界2.HD.720p.韩版中英双字幕.rmvb'
    # all_url = download_address_translation(url)
    # print(all_url)
    # thunder_url = all_url.get('thunder')
    # print(thunder_url)
    download_with_thunder(url)

    # downUrl = 'ftp://ygdy8:ygdy8@yg45.dydytt.net:3116/阳光电影www.ygdy8.com.侏罗纪世界2.HD.720p.韩版中英双字幕.rmvb'
    # os.system("\"F:\\minixunlei\\MiniThunder.exe\" -StartType:DesktopIcon %s" % downUrl)





