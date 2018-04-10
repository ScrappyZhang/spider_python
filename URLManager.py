"""URL管理器"""
'''
@Time    : 2018/4/10 下午8:03
@Author  : scrappy_zhang
@File    : URLManager.py
'''


class UrlManager:
    def __init__(self):
        self.new_urls = set()
        self.old_urls = set()

    def has_new_url(self):
        """
        判断是否有未爬取的URL
        """
        return self.new_url_size()

    def new_url_size(self):
        return len(self.new_urls)

    def get_new_url(self):
        """
        获取一个未爬取的url
        :return:
        """
        new_url = self.new_urls.pop()
        self.old_urls.add(new_url)
        return new_url

    def add_new_url(self, url):
        """
        将新的url添加到未爬取的URL集合
        :param url: 单个URL
        :return:
        """
        if url is None:
            return
        if url not in self.new_urls and url not in self.old_urls:
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
