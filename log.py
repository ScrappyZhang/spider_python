"""log设置"""
'''
@Time    : 2018/4/10 下午11:30
@Author  : scrappy_zhang
@File    : log.py
'''

import logging
from logging import handlers


class Logger(object):
    level_relations = {
        'debug': logging.DEBUG,
        'info': logging.INFO,
        'warning': logging.WARNING,
        'error': logging.ERROR,
        'crit': logging.CRITICAL
    }  # 日志级别关系映射

    def __init__(self, filename='./logs/log',level='info',
                 fmt='%(asctime)s - %(pathname)s[line:%(lineno)d] - %(levelname)s: %(message)s'):
        self.logger = logging.getLogger()
        self.logger.setLevel(self.level_relations.get(level))  # 设置日志级别
        format_str = logging.Formatter(fmt)  # 设置日志格式

        # 创建一个handler，用于写入日志文件
        fh = logging.FileHandler(filename, encoding='utf-8')
        fh.setLevel(self.level_relations.get(level))
        fh.setFormatter(format_str)  # 设置文件里写入的格式
        # 输出到控制台
        sh = logging.StreamHandler()  # 往屏幕上输出
        sh.setLevel(logging.INFO) # 屏幕级别为INFO
        sh.setFormatter(format_str)  # 设置屏幕上显示的格式

        self.logger.addHandler(sh)  # 把对象加到logger里
        self.logger.addHandler(fh)

if __name__ == '__main__':
    log = Logger(filename='./logs/log', level='debug')
    logging.info("111")
    logging.debug("章")
    logging.error("333")
