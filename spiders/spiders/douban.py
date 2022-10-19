import re

import scrapy
from scrapy import Selector, Request
from scrapy.http import HtmlResponse

from spiders.items import MovieItem


class DoubanSpider(scrapy.Spider):
    """豆瓣top250 spider"""
    name = 'douban'
    allowed_domains = ['douban.com']

    def start_requests(self):
        for page in range(1):
            yield scrapy.Request(
                url=f'https://movie.douban.com/top250?start={page * 25}$filter=',
            )

    def parse(self, response: HtmlResponse, **kwargs):
        sel = Selector(response)
        items_list = sel.css('#content > div > div.article > ol > li')
        for item in items_list:
            detail_url = item.css('div.info > div.hd > a::attr(href)').extract_first()   # 电影详情页url
            movie_item = MovieItem()
            movie_item['title'] = item.css('span.title::text').extract_first()
            movie_item['rating'] = item.css('span.rating_num::text').extract_first()
            movie_item['subject'] = item.css('span.inq::text').extract_first()
            yield Request(
                url=detail_url, callback=self.parse_detail,
                cb_kwargs={'item': movie_item}
            )

    def parse_detail(self, response: HtmlResponse, **kwargs):
        """处理详情页面"""
        movie_item = kwargs['item']
        sel = Selector(response)
        movie_item['duration'] = int(sel.css('span[property="v:runtime"]::attr(content)').extract_first())
        movie_item['introduce'] = self.clean_introduce(sel)
        yield movie_item

    @staticmethod
    def clean_introduce(sel):
        introduce_origin = sel.css('span[property="v:summary"]::text').extract_first()
        res = re.sub('[\s]', '', introduce_origin, flags=0)
        return res
