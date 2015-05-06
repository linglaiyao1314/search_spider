# coding=utf-8
import requests
from purl import URL
from lxml import etree
from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL
from filter_help import *
import urlparse
from logs import search_logger


class Item(dict):
    """"""


class Url(object):
    def __init__(self, url):
        self._url = URL(url)

    def get_usual_url(self):
        return str(self._url)

    def get_url_with_parmater(self, parmater, value):
        try:
            return str(getattr(self._url, parmater)(value))
        except AttributeError:
            return self.get_usual_url()

    def set_url_with_parmater(self, parmater, value):
        try:
            self._url = getattr(self._url, parmater)(value)
        except AttributeError:
            pass

    def add_path(self, value):
        self._url = self._url.add_path_segment(value).as_string()

    def __str__(self):
        return str(self._url)


class Spider(object):
    """爬虫基类"""
    def __init__(self, name, start_urls, **kwargs):
        """
        :param name: 爬虫的name
        :param start_urls: 初始url
        """
        self._name = name
        if isinstance(start_urls, list):
            self._urls = start_urls
        elif isinstance(start_urls, str) or isinstance(start_urls, unicode):
            self._urls = [start_urls]
        self.kwargs = kwargs

    def get_urls(self):
        return self._urls

    def make_request(self):
        method = self.kwargs.get("method", "get")
        if not self.kwargs.get("timeout", None):
            self.kwargs["timeout"] = 5

        for url in self._urls:
            kwargs = dict(
                (key, value) for (key, value) in self.kwargs.items() if key in ["method", "params", "json", "headers",
                                                                                "cookies", "files", "auth", "timeout",
                                                                                "allow_redirects", "stream", "verify",
                                                                                "cert"])
            resp = getattr(requests, method)(url, **kwargs)
            search_logger.info("[spider: %s] Request for  '%s' , resp code is %d" %
                               (self._name, resp.url, resp.status_code))
            yield resp

    def get_html_body_by_lxml(self, response):
        """
        根据给定的请求进行转编码处理
        """
        text = unicode(response.content, response.encoding)
        xpath_content = etree.HTML(text)
        return xpath_content


class SearchSpider(Spider):
    """
    通用搜索爬虫，专用于通过简单规则就能直接获取到数据的站点
    """
    def __init__(self, name, start_urls, rule, **kwargs):
        super(SearchSpider, self).__init__(name, start_urls, **kwargs)
        self._rule = rule.get(name, None)
        self._itemlist = []
        self._extract_count = 0

    def parse_item(self, limit):
        rule = self._rule["RuleOfItem"]
        for resp in self.make_request():
            search_logger.info("Spider is [ %s ]" % self._name)
            xbody = self.get_html_body_by_lxml(resp)
            for good_name, price, image_url, good_url in zip(
                    xbody.xpath(rule[GOOD_NAME]), xbody.xpath(rule[PRICE]),
                    xbody.xpath(rule[IMAGE_URL]), xbody.xpath(rule[GOOD_URL])
            ):
                if self._extract_count >= int(limit):
                    break
                try:
                    items = Item(shopid=self.kwargs.get("shopid", 24))
                    items[GOOD_NAME] = good_name
                    items[PRICE] = price
                    items[IMAGE_URL] = image_url
                    items[GOOD_URL] = good_url
                    search_logger.info("%s crawler item" % self._name)
                    search_logger.info(items)
                except:
                    search_logger.error("items crawl wrong....from %s" % self._name, exc_info=True)
                else:
                    self._itemlist.append(items)
                    self._extract_count += 1

    def format_item(self):
        pass

    def get_itemlist(self):
        return self._itemlist

    def length(self):
        return len(self._itemlist)


class CommandSearchSpider(SearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(CommandSearchSpider, self).__init__(name, start_urls, rule, **kwargs)

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            str_items[PRICE] = handler_price(str_items[PRICE])
            str_items[GOOD_URL] = urlparse.urljoin(self._rule['domain'], str_items[GOOD_URL])
            str_items[IMAGE_URL] = urlparse.urljoin(self._rule['domain'], str_items[IMAGE_URL])
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist

