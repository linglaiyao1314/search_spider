# coding=utf-8
import requests
from filter_help import show_state
from purl import URL
from lxml import etree
from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL


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
    def __init__(self, name, start_urls, **kwargs):
        self._name = name
        if isinstance(start_urls, list):
            self._urls = start_urls
        elif isinstance(start_urls, str) or isinstance(start_urls, unicode):
            self._urls = [start_urls]
        self.kwargs = kwargs

    def make_request(self):
        method = self.kwargs.get("method", "get")
        for url in self._urls:
            kwargs = {key: value for key, value in self.kwargs.items() if key in ["method", "params", "json", "headers",
                                                                                  "cookies", "files", "auth", "timeout",
                                                                                  "allow_redirects", "stream", "verify",
                                                                                  "cert"]}

            resp = getattr(requests, method)(url, **kwargs)
            print "%s -> Request for  \n '%s'  \nresp code is %d" % (self._name, resp.url, resp.status_code)
            yield resp


    def get_html_body_by_lxml(self, response):
        """
        根据给定的请求进行转编码处理
        """
        text = unicode(response.content, response.encoding)
        xpath_content = etree.HTML(text)
        return xpath_content


class SearchSpider(Spider):

    def __init__(self, name, start_urls, rule, **kwargs):
        super(SearchSpider, self).__init__(name, start_urls, **kwargs)
        self._rule = rule.get(name, None)
        self._itemlist = []
        self._extract_count = 0

    def parse_item(self, limit):
        rule = self._rule["RuleOfItem"]
        for resp in self.make_request():
            show_state("Spider is ->", self._name)
            xbody = self.get_html_body_by_lxml(resp)
            for good_name, price, image_url, good_url in zip(
                    xbody.xpath(rule[GOOD_NAME]), xbody.xpath(rule[PRICE]),
                    xbody.xpath(rule[IMAGE_URL]), xbody.xpath(rule[GOOD_URL])
            ):
                if self._extract_count >= int(limit):
                    break
                try:
                    items = Item(shopid=self.kwargs.get("shopid", 1))
                    items[GOOD_NAME] = good_name
                    items[PRICE] = price
                    items[IMAGE_URL] = image_url
                    items[GOOD_URL] = good_url
                    show_state("%s crawler item" % self._name, items)
                except:
                    show_state("ERROR", "items crawl wrong....")
                else:
                    self._itemlist.append(items)
                    self._extract_count += 1

    def format_item(self):
        pass

    def get_itemlist(self):
        return self._itemlist

    def length(self):
        return len(self._itemlist)


