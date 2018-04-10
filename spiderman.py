"""爬虫调度"""
'''
@Time    : 2018/4/10 下午9:02
@Author  : scrappy_zhang
@File    : spiderman.py
'''
from DataOputput import DataOutput
from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParparser
from URLManager import UrlManager

import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s %(filename)s[line:%(lineno)d] %(levelname)s %(message)s',
                    datefmt='%a, %d %b %Y %H:%M:%S',
                    filemode='w',
                    filename='./test.log')


class SpiderMan(object):
    def __init__(self):
        self.manager = UrlManager()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParparser()
        self.output = DataOutput()

    def crawl(self, root_url):
        # 1. 添加入口URL
        self.manager.add_new_url(root_url)
        while (self.manager.has_new_url() and self.manager.old_url_size() < 100):
            try:
                new_url = self.manager.get_new_url()
                html = self.downloader.download(new_url)
                new_urls, data = self.parser.parser(new_url, html)
                self.manager.add_new_urls(new_urls)
                self.output.store_data(data)
                logging.info("done %s page " % self.manager.old_url_size())
            except Exception as e:
                logging.error(e)
                print("crawl failed")

        self.output.output_html()


if __name__ == '__main__':
    spider_man = SpiderMan()
    spider_man.crawl("https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB")
