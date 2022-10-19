import re

import scrapy

from spiders.items import GraphicsItem


class JdmallSpider(scrapy.Spider):
    """京东显卡数据 spider"""
    name = 'jdmall'
    allowed_domains = ['search.jd.com']

    def start_requests(self):
        for i in range(10):
            if i == 0:
                count = 1
            elif i == 1:
                count = 56
            else:
                count = 56 + (i - 1) * 60
            yield scrapy.Request(
                url=f'https://search.jd.com/Search?keyword=%E6%98%BE%E5%8D%A1&wq=%E6%98%BE%E5%8D%A1&pvid'
                    f'=cc81a5c0cc1b4ee592a95304021da0ef&page={2*i + 1}&s={count}&click=0 '
            )

    def parse(self, response, **kwargs):
        sel = scrapy.Selector(response)
        items_list = sel.css('#J_goodsList > ul > li')
        print(len(items_list))
        print("==================================================")
        for item in items_list:
            detail_url = 'https://' + item.css('div > div.p-img > a::attr(href)').extract_first()  # 显卡详情页url
            graphics_item = GraphicsItem()
            graphics_item['price'] = int(item.css('div > div.p-price > strong > i::text').extract_first().split('.')[0])
            graphics_item['link'] = detail_url
            yield scrapy.Request(
                url=detail_url, callback=self.parse_detail,
                cb_kwargs={'item': graphics_item}
            )

    @staticmethod
    def parse_detail(response, **kwargs):
        graphics_item = kwargs['item']
        sel = scrapy.Selector(response)
        origin_text = sel.css('div.itemInfo-wrap > div.sku-name::text').extract_first()
        graphics_item['model'] = re.sub('[\s]', '', origin_text, flags=0)
        yield graphics_item
