# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
import openpyxl
import pymysql

from scrapy.crawler import Crawler


class SpidersPipelineToMysqlJdMall:
    """
    显卡信息写入mysql
    """
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        host = crawler.settings['JDDB_HOST']
        port = crawler.settings['JDDB_PORT']
        username = crawler.settings['JDDB_USER']
        password = crawler.settings['JDDB_PASSWD']
        database = crawler.settings['JDDB_NAME']
        return cls(host, port, username, password, database)

    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(host=host, port=port,
                                    user=username, password=password,
                                    database=database, charset='utf8mb4',
                                    autocommit=True)
        self.cursor = self.conn.cursor()
        self.data = list()

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.__write_to_jd_mysql()
        self.conn.close()

    def process_item(self, item, spider):
        model = item.get('model', '')
        price = item.get('price', 0)
        link = item.get('link', '')
        self.data.append((model, price, link))
        if len(self.data) == 100:
            self.__write_to_jd_mysql()
            self.data.clear()
        return item

    def __write_to_jd_mysql(self):
        self.cursor.executemany(
            'insert into graphics_jd (model, price, link) values (%s, %s, %s)',
            self.data
        )


class SpidersPipelineToMysqlDouban:
    """
    将结果写入mysql
    """
    @classmethod
    def from_crawler(cls, crawler: Crawler):
        host = crawler.settings['DOUBANDB_HOST']
        port = crawler.settings['DOUBANDB_PORT']
        username = crawler.settings['DOUBANDB_USER']
        password = crawler.settings['DOUBANDB_PASSWD']
        database = crawler.settings['DOUBANDB_NAME']
        return cls(host, port, username, password, database)

    def __init__(self, host, port, username, password, database):
        self.conn = pymysql.connect(host=host, port=port,
                                    user=username, password=password,
                                    database=database, charset='utf8mb4',)
        self.cursor = self.conn.cursor()
        self.data = list()

    def close_spider(self, spider):
        if len(self.data) > 0:
            self.__write_to_douban_mysql()
        self.conn.close()

    def process_item(self, item, spider):
        title = item.get('title', '')
        rating = item.get('rating', 0)
        subject = item.get('subject', '')
        duration = item.get('duration', 0)
        introduce = item.get('introduce', '')
        self.data.append((title, rating, subject, duration, introduce))
        if len(self.data) == 100:
            self.__write_to_douban_mysql()
            self.data.clear()
        return item

    def __write_to_douban_mysql(self):
        self.cursor.executemany(
            'insert into top_movie (title, rating, subject, duration, introduce) values (%s, %s, %s, %s, %s)',
            self.data
        )
        self.conn.commit()


class SpidersPipelineToExcelDouban:
    """
    将结果写入excel表
    """
    def __init__(self):
        self.wb = openpyxl.Workbook()
        self.ws = self.wb.active
        self.ws.title = 'top250'
        self.ws.append(('标题', '评分', '主题', '时长', '简介'))

    def close_spider(self, spider):
        self.wb.save('电影数据.xlsx')

    def process_item(self, item, spider):
        title = item.get('title', '')
        rating = item.get('rating', 0)
        subject = item.get('subject', '')
        duration = item.get('duration', 0)
        introduce = item.get('introduce', '')
        self.ws.append((title, rating, subject, duration, introduce))
        return item
