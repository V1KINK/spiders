# Define here the models for your spider middleware
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/spider-middleware.html
import scrapy.http
from scrapy import signals
from utils import create_chrome_driver

# useful for handling different item types with a single interface
from itemadapter import is_item, ItemAdapter


cookie_str_douban = 'll="118371"; bid=Yy462KgIjLU; __gads=ID=4c6161ca78b3081f-223fc68398d4003f:T=1655553533:RT' \
             '=1655553533:S=ALNI_MZM8_wG57CzmZU8FKZ3j2WL8kZy-A; ' \
             '_pk_ref.100001.8cb4=%5B%22%22%2C%22%22%2C1663990252%2C%22https%3A%2F%2Fwww.baidu.com%2Flink%3Furl' \
             '%3DQXUurATS9xpsHBxNSqRMkCX-pFdOIkyrN27DDSNgQJJPt1pKOIsmAuXuLrRkGAe_%26wd%3D%26eqid' \
             '%3Db91f0e230000b7ab00000004632e79e9%22%5D; _pk_ses.100001.8cb4=*; ' \
             '__utma=30149280.191273945.1655553532.1663650788.1663990254.4; __utmc=30149280; ' \
             '__utmz=30149280.1663990254.4.4.utmcsr=baidu|utmccn=(organic)|utmcmd=organic; ap_v=0,' \
             '6.0; __gpi=UID=000006c03dcf7088:T=1655553533:RT=1663990256:S=ALNI_Mb1BY110YfCexkTAf2yhI9lftyPeg; ' \
             'ct=y; push_noty_num=0; push_doumail_num=0; __utmv=30149280.26306; ' \
             '__yadk_uid=qp8dcPgYlz1ng19gaCETUoN5RlFbaoc0; dbcl2="263064275:OcQ8dShFgh4"; ck=x3j6; __utmt=1; ' \
             '_pk_id.100001.8cb4=68d74407fc065f1c.1663402660.2.1663991956.1663402662.; ' \
             '__utmb=30149280.17.10.1663990254 '

cookie_str_jdmall = 'unpl=JF8EAK1nNSttDBlUBhxVHhZESFwDW1hfSkRWaWAEXFxQG1JSGQEaQRN7XlVdXhRLFh9uYRRVVFNPXQ4aASsSEXteXVdZ' \
                    'DEsWC2tXVgQFDQ8VXURJQlZAFDNVCV9dSRZRZjJWBFtdT1xWSAYYRRMfDlAKDlhCR1FpMjVkXlh7VAQrBxoWEUpUU1haOHsQM' \
                    '19XAFxbX0tUNRoyGiJSHwFXXVoJSxVOamYBVVxRTFICKwMrEQ;' \
                    ' __jdv=76161171|baidu-pinzhuan|t_288551095_baidupinzhuan|cpc|0f3d30c8dba7459bb52f2eb5eba8ac7d_0_e' \
                    'c126f45e20f44f0bd760909a7f320b2|1665104283478; __jdu=405008676; areaId=28; ipLoc-djd=28-2534-0-0;' \
                    ' PCSYCityID=CN_620000_621200_0;' \
                    ' shshshfpa=97cf0306-208a-2a28-5077-5e5f69e09e88-1665104284;' \
                    ' shshshfpb=iTETGwhtP2bcPi75s4m77Rw;' \
                    ' __jda=122270672.405008676.1665104281.1665104281.1665104283.1;' \
                    ' __jdb=122270672.2.405008676|1.1665104283;' \
                    ' __jdc=122270672; jsavif=1; jsavif=1;' \
                    ' shshshfp=94313309aa2eaf5c7f95d1fff9590ab8;' \
                    ' shshshsID=ef68aba0d69cee542094beee67269c4f_2_1665104295531;' \
                    ' rkv=1.0; qrsc=1;' \
                    ' 3AB9D23F7A4B3C9B=E26H6HICFVRA45DERHQ7TJEZEADGRNQUQLARG4DKOYGPVT646XSCYDKFFGD6BASRFZXDFAIGTVAJRP2' \
                    'I3H3BAGYW44'


def get_cookie_dict(cookie_str):
    cookie_dict = dict()

    for item in cookie_str.split('; '):
        key, value = item.split("=", maxsplit=1)
        cookie_dict[key] = value
    return cookie_dict


COOKIE_DICT_DOUBAN = get_cookie_dict(cookie_str_douban)
COOKIE_DICT_JDMALL = get_cookie_dict(cookie_str_jdmall)


class SpidersSpiderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the spider middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_spider_input(self, response, spider):
        # Called for each response that goes through the spider
        # middleware and into the spider.

        # Should return None or raise an exception.
        return None

    def process_spider_output(self, response, result, spider):
        # Called with the results returned from the Spider, after
        # it has processed the response.

        # Must return an iterable of Request, or item objects.
        for i in result:
            yield i

    def process_spider_exception(self, response, exception, spider):
        # Called when a spider or process_spider_input() method
        # (from other spider middleware) raises an exception.

        # Should return either None or an iterable of Request or item objects.
        pass

    def process_start_requests(self, start_requests, spider):
        # Called with the start requests of the spider, and works
        # similarly to the process_spider_output() method, except
        # that it doesn’t have a response associated.

        # Must return only requests (not items).
        for r in start_requests:
            yield r

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpidersDownloaderMiddleware:
    # Not all methods need to be defined. If a method is not defined,
    # scrapy acts as if the downloader middleware does not modify the
    # passed objects.

    @classmethod
    def from_crawler(cls, crawler):
        # This method is used by Scrapy to create your spiders.
        s = cls()
        crawler.signals.connect(s.spider_opened, signal=signals.spider_opened)
        return s

    def process_request(self, request, spider):
        # Called for each request that goes through the downloader
        # middleware.

        # Must either:
        # - return None: continue processing this request
        # - or return a Response object
        # - or return a Request object
        # - or raise IgnoreRequest: process_exception() methods of
        #   installed downloader middleware will be called
        return None

    def process_response(self, request, response, spider):
        # Called with the response returned from the downloader.

        # Must either;
        # - return a Response object
        # - return a Request object
        # - or raise IgnoreRequest
        return response

    def process_exception(self, request, exception, spider):
        # Called when a download handler or a process_request()
        # (from other downloader middleware) raises an exception.

        # Must either:
        # - return None: continue processing this exception
        # - return a Response object: stops process_exception() chain
        # - return a Request object: stops process_exception() chain
        pass

    def spider_opened(self, spider):
        spider.logger.info('Spider opened: %s' % spider.name)


class SpidersDownloaderMiddlewareDouban(SpidersDownloaderMiddleware):
    """豆瓣下载中间件"""
    def process_request(self, request, spider):
        request.cookies = COOKIE_DICT_DOUBAN
        return None


class SpidersDownloaderMiddlewareJd(SpidersDownloaderMiddleware):
    """京东下载中间件"""
    def __init__(self):
        self.browser = create_chrome_driver()

    def __del__(self):
        self.browser.close()

    def process_request(self, request, spider):
        self.browser.get(request.url)
        return scrapy.http.HtmlResponse(url=request.url, body=self.browser.page_source,
                                        request=request, encoding='utf-8')

