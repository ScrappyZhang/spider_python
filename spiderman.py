"""爬虫调度"""
'''
@Time    : 2018/4/10 下午9:02
@Author  : scrappy_zhang
@File    : spiderman.py
'''

from HtmlDownloader import HtmlDownloader
from HtmlParser import HtmlParparser

import logging

from log import Logger
from multiprocessing.managers import BaseManager


class SpiderWork(object):
    def __init__(self):
        BaseManager.register("get_task_queue")
        BaseManager.register("get_result_queue")
        server_addr = "127.0.0.1"
        logging.info('Connect to server %s ...' % server_addr)
        self.m = BaseManager(address=(server_addr, 8001), authkey="baike".encode())
        self.m.connect()
        self.task = self.m.get_task_queue()
        self.result = self.m.get_result_queue()
        self.downloader = HtmlDownloader()
        self.parser = HtmlParparser()
        logging.info("init finish")

    def crawl(self):
        while (True):
            try:
                if not self.task.empty():
                    url = self.task.get()

                    if url == 'end':
                        logging.info("控制节点通知爬虫节点停止工作")
                        self.result.put(dict(new_urls="end", data="end"))
                        return
                    logging.info("爬虫节点正在解析：%s" % url.encode('utf-8'))
                    content = self.downloader.download(url)
                    new_urls, data = self.parser.parser(url, content)
                    self.result.put(dict(new_urls=new_urls, data=data))
            except EOFError as e:
                logging.info("连接工作节点失败")
                return
            except Exception as e:
                logging.error(e)
                logging.info("Craw failed")


if __name__ == '__main__':
    Logger('./logs/spiderwork.log', level='debug')
    spider_man = SpiderWork()
    spider_man.crawl()
