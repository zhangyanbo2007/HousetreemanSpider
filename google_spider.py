# date：2020.5.25
# author:pmy
# aim:爬取google图片
#问题在于，不能保证所爬为所见

from selenium import webdriver
import time
import os
import requests

# 修改keyword便可以修改搜索关键词 建议也修改存储目录
keyword = 'cat'
# url = 'https://www.google.com.hk/search?q=' + keyword + '&source=lnms&tbm=isch'
url = 'https://www.google.com/search?q=' + keyword + '&source=lnms&tbm=isch'


class Crawler_google_images:
    # 初始化
    def __init__(self):
        self.url = url

    # 获得Chrome驱动，并访问url
    def init_browser(self):
        chrome_options = webdriver.ChromeOptions()
        chrome_options.add_argument("--disable-infobars")
        browser = webdriver.Chrome(chrome_options=chrome_options)
        # 访问url
        browser.get(self.url)
        # 最大化窗口，之后需要爬取窗口中所见的所有图片
        browser.maximize_window()
        return browser

    # 下载图片
    def download_images(self, browser, num=100):
        #存储路径
        picpath = './cat'
        # 路径不存在时创建一个
        if not os.path.exists(picpath): os.makedirs(picpath)

        count = 0  # 图片序号
        pos = 0
        # print(num)

        while (True):
            try:
                # 向下滑动
                js = 'var q=document.documentElement.scrollTop=' + str(pos)
                pos += 500
                browser.execute_script(js)
                time.sleep(1)
                # 找到图片
                # html = browser.page_source#也可以抓取当前页面的html文本，然后用beautifulsoup来抓取
                # 直接通过tag_name来抓取是最简单的，比较方便
                img_elements = browser.find_elements_by_xpath('//a[@class="wXeWr islib nfEiy mM5pbd"]')
                try:
                    for img_element in img_elements:
                        #点开大图页面
                        img_element.click()
                        time.sleep(0.5)
                        try:
                            # 这里balabala里面有好几个，所以要过滤一下
                            # 取名好烦哦···
                            balabalas = browser.find_elements_by_xpath('//img[@class="n3VNCb"]')

                            if (balabalas):
                                for balabala in balabalas:
                                    src = balabala.get_attribute('src')
                                    #过滤掉缩略图和无关干扰信息
                                    if src.startswith('http') and not src.startswith(
                                            'https://encrypted-tbn0.gstatic.com'):
                                        print('Found' + str(count) + 'st image url')
                                        # img_url_dic.append(src)
                                        self.save_img(count, src, picpath)
                                        count += 1
                                        #爬取到指定数量图片后退出
                                        if (count >= num):
                                            return "stop"
                        except:
                            print('获取图片失败')

                    #回退
                    browser.back()
                    time.sleep(0.3)
                except:
                    print('获取页面失败')
            except:
                print("划不动了")

    def save_img(self, count, img_src, picpath):
        filename = picpath + '/' + str(count) + '.jpg'
        r = requests.get(img_src)
        with open(filename, 'wb') as f:
            f.write(r.content)
        f.close()

    def run(self):
        self.__init__()
        browser = self.init_browser()
        self.download_images(browser, 100)  # 可以修改爬取的图片数
        browser.close()
        print("############爬取完成")


if __name__ == '__main__':
    craw = Crawler_google_images()
    craw.run()