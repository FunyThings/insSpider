# -*- coding:utf-8 -*-


#环境python2.7，
#python3.6不支持phantomjs
import json
from selenium import webdriver
# 引入配置对象DesiredCapabilities
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

from lxml import etree
import time
import random
#单元测试模块
import unittest

class ins(unittest.TestCase):
    #初始化方法
    def setUp(self):
        headers = {
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
            'Accept-Language': 'zh-CN,zh;q=0.8,en-US;q=0.5,en;q=0.3',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_12_5) AppleWebKit/603.2.4 (KHTML, like Gecko) Version/10.1.1 Safari/603.2.4',
            'Connection': 'keep-alive'
        }
        self.dcap = DesiredCapabilities.PHANTOMJS.copy()

        for key, value in headers.items():
            self.dcap['phantomjs.page.customHeaders.{}'.format(key)] = value

        self.driver = webdriver.PhantomJS(desired_capabilities=self.dcap)
        #浏览器最大化
        self.driver.maximize_window()

        self.list = []
        self.i = 0

    #测试方法
    def testIns(self):
        #访问ins
        self.driver.get("https://www.instagram.com/ahmad_monk/")

        print self.driver.title
        # 等待加载20s
        time.sleep(10)
        # 点击‘更多’，继续加载
        self.driver.find_element_by_class_name("_1cr2e").click()
        # 等待加载
        time.sleep(random.randint(20,30))
        #滚动加载30次，经测试可以拉到底部
        for i in range(1,30):
            i = i*5000
            js1 = "var q=document.body.scrollTop=" +str(i)
            self.driver.execute_script(js1)
            time.sleep(random.randint(10, 15))
        self.driver.save_screenshot("ins8.png")
        #解析整个有全部图片的页面
        html = etree.HTML(self.driver.page_source)
        #提取详情页url
        urls = html.xpath("//div[@class='_mck9w _gvoze _f2mse']/a/@href")
        #循环进入详情页
        for url in urls:
            full_url = "https://www.instagram.com"+url
            self.driver.get(full_url)
            time.sleep(random.randint(20, 30))
            #刷新页面，不刷新的话，会停在当前页弹出框，部分内容无法加载
            self.driver.refresh()
            print("进入页面 " +str(self.i) +"  " + full_url)
            self.i += 1
            time.sleep(random.randint(20, 30))
            #解析详情页
            imghtml = etree.HTML(self.driver.page_source)
            #图片地址
            src = imghtml.xpath("//div[@class='_4rbun']/img/@src")
            print(src)
            #点赞
            point = imghtml.xpath("//span[@class='_nzn1h']/span/text()")
            print(point)
            #更新日期
            day = imghtml.xpath("//time[@class='_p29ma _6g6t5']/@title")
            print(day)
            #以字典形式加入列表
            self.list.append({"imgUrl": src, "imgPoint": point, "imgUpday": day})
            #打开文件，写入json数据
            with open('insdata.json', 'wb+') as file:
                text = json.dumps(self.list, ensure_ascii=False).encode("utf-8")
                file.write(text)
            file.close()
            time.sleep(random.randint(5, 15))

    #退出
    def tearDown(self):
        #退出浏览器
        self.driver.quit()


if __name__ == "__main__":
    # 启动测试模块
    unittest.main()

