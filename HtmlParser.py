"""HTML解析器"""
'''
@Time    : 2018/4/10 下午8:33
@Author  : scrappy_zhang
@File    : HtmlParser.py
'''

import re
import urllib.parse

from bs4 import BeautifulSoup
import logging


class HtmlParparser:
    def parser(self, page_url, html_content):
        """
        用于解析内容，抽取url和摘要标题
        :param page_url: 下载页面URL
        :param html_content: 下载页面内容
        :return: 返回URL和数据
        """
        if page_url is None or html_content is None:
            return
        soup = BeautifulSoup(html_content, "html.parser")
        new_urls = self._get_new_urls(page_url, soup)
        new_data = self._get_new_data(page_url, soup)
        return new_urls, new_data

    def _get_new_urls(self, page_url, soup):
        """
        抽取新的URL集合
        :param page_url: 下载页面基URL
        :param soup: soup
        :return: 返回新的url集合
        """
        new_urls = set()
        try:
            links = soup.find_all("a", href=re.compile(r'^/item/.*'))
        except Exception as e:
            logging.error(e)
        else:
            for link in links:
                new_url = link['href']
                new_full_url = urllib.parse.urljoin(page_url, new_url)
                new_urls.add(new_full_url)
        return new_urls

    def _get_new_data(self, page_url, soup):
        """
        抽取有效数据
        :param page_url: 下载页面URL
        :param soup: soup
        :return: 有效数据
        """
        data = {}
        data['url'] = page_url
        try:
            title = soup.find('dd', class_="lemmaWgt-lemmaTitle-title").find('h1')
        except Exception as e:
            logging.error(e)
        else:
            data['title'] = title.get_text()
        try:
            summary = soup.find('div', attrs={'class': "para", 'label-module': "para"})
        except Exception as e:
            logging.error(e)
        else:
            data['summary'] = summary.get_text()
        return data


if __name__ == '__main__':
    base_url = 'https://baike.baidu.com/%E7%BB%9C%E7%88%AC%E8%99%AB/5162711?fr=aladdin'
    new_url = "/item/%E7%BD%91%8%AC%E8%99%AB/"
    print(urllib.parse.urljoin(base_url, new_url))
