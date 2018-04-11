"""分布式管理器"""
'''
@Time    : 2018/4/11 下午2:00
@Author  : scrappy_zhang
@File    : nodemanager.py
'''
import logging
import time
from log import Logger

from multiprocessing import Queue
from multiprocessing.managers import BaseManager
from multiprocessing import Process

from URLManager import UrlManager
from DataOputput import DataOutput


class NodeManager(object):
    def start_manager(self, url_q, result_q):
        """
        创建一个分布式管理器
        :param url_q: URL队列
        :param result_q: 爬虫结果队列
        :return:
        """
        BaseManager.register("get_task_queue", callable=lambda: url_q)
        BaseManager.register("get_result_queue", callable=lambda: result_q)
        manager = BaseManager(address=("", 8001), authkey="baike".encode())
        return manager

    def url_manager_proc(self, url_q, conn_q, root_url):
        """从conn_q队列获取新URL到URL管理器， 取URL放入url_q供爬虫节点获取"""
        url_manager = UrlManager()
        url_manager.add_new_url(root_url)
        while True:
            while (url_manager.has_new_url()):
                new_url = url_manager.get_new_url()
                url_q.put(new_url)
                logging.info("old_url_size = %s " % url_manager.old_url_size())

                if url_manager.old_url_size() > 50:
                    url_q.put("end")
                    logging.info("控制节点发起结束通知")
                    url_manager.save_process("new_urls.txt", url_manager.new_urls)
                    url_manager.save_process("old_urls.txt", url_manager.old_urls)
                    return
            try:
                if not conn_q.empty():
                    urls = conn_q.get()
                    url_manager.add_new_urls(urls)
            except BaseException as e:
                time.sleep(0.1)

    def result_solve_proc(self, result_q, conn_q, store_q):
        while (True):
            try:
                if not result_q.empty():
                    content = result_q.get(True)
                    if content['new_urls'] == "end":
                        logging.info("结果处理进程得到通知后结束...")
                        store_q.put("end")
                        return
                    conn_q.put(content['new_urls'])
                    store_q.put(content['data'])
                else:
                    time.sleep(0.1)
            except BaseException as e:
                logging.info(e)
                time.sleep(0.1)

    def store_proc(self, store_q):
        output = DataOutput()
        while True:
            if not store_q.empty():
                data = store_q.get()
                if data == "end":
                    logging.info("存储进程接收到节点通知后结束")
                    output.output_end(output.filepath)

                    return
                output.store_data(data)
            else:
                time.sleep(0.1)


if __name__ == '__main__':
    Logger('./logs/nodemanager.log', level='debug')
    # 1. 初始化4个队列
    url_q = Queue()
    result_q = Queue()
    conn_q = Queue()
    store_q = Queue()

    # 2. 创建分布式管理器
    node = NodeManager()
    manager = node.start_manager(url_q, result_q)

    # 3. 创建URL管理进程、数据提取进程和数据存储进程
    url_manager_proc = Process(target=node.url_manager_proc, args=(
    url_q, conn_q, "https://baike.baidu.com/item/%E7%BD%91%E7%BB%9C%E7%88%AC%E8%99%AB"))
    result_solve_proc = Process(target=node.result_solve_proc, args=(result_q, conn_q, store_q))
    store_proc = Process(target=node.store_proc, args=(store_q,))

    # 4. 启动进程和管理器
    url_manager_proc.start()
    result_solve_proc.start()
    store_proc.start()

    manager.get_server().serve_forever()
