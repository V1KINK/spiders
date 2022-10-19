# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class MovieItem(scrapy.Item):
    """
    组织电影item数据
    """
    title = scrapy.Field()
    rating = scrapy.Field()
    subject = scrapy.Field()
    duration = scrapy.Field()
    introduce = scrapy.Field()


class GraphicsItem(scrapy.Item):
    """
    组织显卡item数据
    """
    model = scrapy.Field()
    price = scrapy.Field()
    link = scrapy.Field()

