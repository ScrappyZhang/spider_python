"""数据存储器"""
'''
@Time    : 2018/4/10 下午8:57
@Author  : scrappy_zhang
@File    : DataOputput.py
'''

import codecs
import time


class DataOutput(object):
    def __init__(self):
        self.filepath = 'baike_%s.html' % (time.strftime("%Y_%m_%d_%H_%M_%S", time.localtime()))
        self.output_head(self.filepath)
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)
        if len(self.datas) > 10:
            self.output_html(self.filepath)

    def output_head(self, path):
        """
        将html头写入
        :param path:
        :return:
        """
        with codecs.open(path, 'w', encoding='utf-8') as fout:
            fout.write("<html>")
            fout.write(
                '<head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title>python3 spider百度搜索</title></head>')
            fout.write("<body>")
            fout.write("<table>")

    def output_html(self, path):
        with codecs.open(path, 'a', encoding='utf-8') as fout:
            for data in self.datas:
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data['url'])
                fout.write("<td>%s</td>" % data['title'])
                fout.write("<td>%s</td>" % data['summary'])
                fout.write("</tr>")
                self.datas.remove(data)

    def output_end(self, path):
        """
        将html尾写入
        :param path:
        :return:
        """
        with codecs.open(path, 'a', encoding='utf-8') as fout:
            fout.write("</table>")
            fout.write("</body>")
            fout.write("</html>")
