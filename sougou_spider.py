import requests
import urllib
import json
import os
import shutil  # 用来删除文件夹
import datetime
from urllib import parse


def getSogouImag(path, keyword, page_num, per_page_num):
    # 判断文件夹是否存在，存在则删除
    if os.path.exists(path):
        shutil.rmtree(path)
    # 创建文件夹
    os.mkdir(path)
    m = 0
    keyword_encoder = parse.quote(keyword.encode('utf-8'))
    for i in range(0, page_num):
        start_p = i*per_page_num
        stop_p = (i+1)*per_page_num
        ##这个 URL 怎么写？ 请看下文解释
        url_i = 'https://pic.sogou.com/napi/pc/searchList?mode=1&start=' \
                + str(start_p) \
                + '&xml_len=' \
                + str(stop_p) \
                + '&query=' + keyword_encoder
        try:
            imgs = requests.get(url_i)
            imgs_text = imgs.text
            imgs_json = json.loads(imgs_text)
            imgs_json = imgs_json['data']
            imgs_items = imgs_json['items']
            for i in imgs_items:
                try:
                    img_url = i['picUrl']
                    print('*********' + str(m) + '.png********' + 'Downloading...')
                    print('下载的url: ', img_url)
                    urllib.request.urlretrieve(img_url, os.path.join(path, str(m) + '.jpg'))
                    m = m + 1
                except:
                    continue
        except:
            continue
    print('Download complete !')


time_stamp = datetime.datetime.now()
print('===start=== at:', time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))

# 循环爬取，每次100张，共10000次
getSogouImag(path='data/sougou_treeman_0701',
             keyword="房树人",
             page_num=100000,
             per_page_num=100)

time_stamp = datetime.datetime.now()
print('===end=== at:', time_stamp.strftime('%Y.%m.%d-%H:%M:%S'))