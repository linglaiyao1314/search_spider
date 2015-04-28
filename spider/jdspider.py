# coding=utf-8
from engin.Spider import Item, CommandSearchSpider
from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL
from engin.filter_help import *
import json
import requests
from lxml import etree


class JdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(JdSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.pattern = r'{"available.*?}'

    def get_all(self, body):
        return re.findall(self.pattern, body)

    def parse_item(self, limit):
        for resp in self.make_request():
            goods = self.get_all(resp.content)
            search_logger.info("request for items in 京东...")
            for element in goods:
                if self._extract_count >= int(limit):
                    break
                element = json.loads(element)
                items = Item(shopid=self.kwargs.get("shopid", 1))
                items[GOOD_NAME] = element['wname']
                items[PRICE] = element['jdPrice']
                items[IMAGE_URL] = element['imageurl']
                items[GOOD_URL] = "http://item.m.jd.com/ware/view.action?wareId=%s" % element['wareId']
                search_logger.debug("item is %s" % items)
                self._itemlist.append(items)
                self._extract_count += 1

    def format_item(self):
        itemlist = []
        cate = self.get_cate(self.kwargs["params"]["keyword"])
        search_logger.info("already catach %d items, and request for cate.... cate is [ %s ] "
                           % (len(self.get_itemlist()), cate))
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            str_items[PRICE] = handler_price(str_items[PRICE])
            str_items[IMAGE_URL] = str_items[IMAGE_URL].replace('n4', 'n7', 1)
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL], cate])
        return itemlist

    def get_cate(self, searchwords):
        search_url = "http://search.jd.com/Search?keyword=%s&enc=utf-8" % searchwords
        with request_open(requests.get(search_url), "") as resp:
            xbody = etree.HTML(resp.content)
            name = xbody.xpath("//div[@class='item fore hover']/h3//a//text()")[0]
            return name




