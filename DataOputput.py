"""数据存储器"""
'''
@Time    : 2018/4/10 下午8:57
@Author  : scrappy_zhang
@File    : DataOputput.py
'''

import codecs


class DataOutput(object):
    def __init__(self):
        self.datas = []

    def store_data(self, data):
        if data is None:
            return
        self.datas.append(data)

    def output_html(self):
        with codecs.open('baike.html', 'w', encoding='utf-8') as fout:
            fout.write("<html>")
            fout.write('<head><meta http-equiv="content-type" content="text/html;charset=utf-8"><title>python3 spider百度搜索</title></head>')
            fout.write("<body>")
            fout.write("<table>")
            for data in self.datas:
                fout.write("<tr>")
                fout.write("<td>%s</td>" % data['url'])
                fout.write("<td>%s</td>" % data['title'])
                fout.write("<td>%s</td>" % data['summary'])
                fout.write("</tr>")
                self.datas.remove(data)
            fout.write("</table>")
            fout.write("</body>")
            fout.write("</html>")
