"""HTML下载器"""
'''
@Time    : 2018/4/10 下午8:11
@Author  : scrappy_zhang
@File    : HtmlDownloader.py
'''

import requests
import chardet

from fake import get_user_agent


class HtmlDownloader:

    def download(self, url):
        user_agent = get_user_agent()
        headers = {
            "User-Agent": user_agent
        }
        if url is None:
            return None
        ret = requests.get(url, headers=headers)

        if 200 == ret.status_code:
            ret.encoding = chardet.detect(ret.content)['encoding']
            return ret.text
        return None

