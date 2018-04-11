"""URL管理器"""
'''
@Time    : 2018/4/10 下午8:03
@Author  : scrappy_zhang
@File    : URLManager.py
'''

import pickle
import hashlib
import logging


class UrlManager:
    def __init__(self):
        self.new_urls = self.load_process('new_urls.txt')
        self.old_urls = self.load_process('old_urls.txt')

    def has_new_url(self):
        """
        判断是否有未爬取的URL
        """
        return self.new_url_size() != 0

    def new_url_size(self):
        return len(self.new_urls)

    def get_new_url(self):
        """
        获取一个未爬取的url
        :return:
        """
        new_url = self.new_urls.pop()
        m = hashlib.md5()
        m.update(new_url.encode())
        self.old_urls.add(m.hexdigest()[8:-8])
        return new_url

    def add_new_url(self, url):
        """
        将新的url添加到未爬取的URL集合
        :param url: 单个URL
        :return:
        """
        if url is None:
            return
        m = hashlib.md5()
        m.update(url.encode())
        url_md5 = m.hexdigest()[8:-8]
        if url not in self.new_urls and url_md5 not in self.old_urls:
            self.new_urls.add(url)

    def add_new_urls(self, urls):
        """
        将新的url添加到未爬取的URL集合
        :param urls: 多个URL集合
        :return:
        """
        if urls is None or len(urls) == 0:
            return
        for url in urls:
            self.add_new_url(url)

    def old_url_size(self):
        return len(self.old_urls)

    def load_process(self, path):
        try:
            with open(path, 'rb') as f:
                tmp = pickle.load(f)
                return tmp
        except Exception as e:
            logging.info(e)
        return set()

    def save_process(self, path, data):
        with open(path, 'wb') as f:
            pickle.dump(data, f)
