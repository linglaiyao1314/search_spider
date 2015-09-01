# coding=utf-8
from engin.Spider import Item, CommandSearchSpider
from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL
from engin.filter_help import *
import json
import requests
from lxml import etree
import urlparse
import chardet


# 手机端京东爬虫
class JdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(JdSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.pattern = r'{"available.*?}'

    def get_all(self, body):
        return re.findall(self.pattern, body)

    def parse_item(self):
        for resp in self.make_request():
            goods = self.get_all(resp.content)
            search_logger.info("request for items in 京东...")
            for element in goods:
                if self._extract_count >= int(self.limit):
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
            str_items = dict((key, value.strip()) for key, value in items.items() if hasattr(value, "strip"))
            str_items[PRICE] = handler_price(str_items[PRICE])
            str_items[IMAGE_URL] = str_items[IMAGE_URL].replace('n4', 'n7', 1)
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL], cate])
        return itemlist

    def get_cate(self, searchwords):
        search_url = "http://search.jd.com/Search?keyword=%s&enc=utf-8" % searchwords
        with request_open(requests.get(search_url), "Request failed Can't catch the cate....") as resp:
            xbody = etree.HTML(resp.content)
            name = xbody.xpath("//div[@class='item fore hover']/h3//a//text()")[0]
            return name


# pc端京东爬虫
class JdSpiderPc(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(JdSpiderPc, self).__init__(name, start_urls, rule, **kwargs)

    def get_html_body_by_lxml(self, response):
        try:
            # xpath_content = etree.HTML(unicode(response.content, response.encoding))
            # xpath_content = etree.HTML(response.content)
            xpath_content = etree.HTML(unicode(response.content, chardet.detect(response.content).get("encoding", "utf8")))
        except:
            xpath_content = etree.HTML(response.content)
        return xpath_content

    def parse_item(self):
        rule = self._rule["RuleOfItem"]
        for resp in self.make_request():
            xbody = self.get_html_body_by_lxml(resp)
            cate = self.get_cate(xbody)
            search_logger.info("request for cate....and cate is [ %s ]" % cate)
            search_logger.info("request for items in [ 京东 ]")
            for good_name, price, image_url, good_url in zip(
                    xbody.xpath(rule[GOOD_NAME]), xbody.xpath(rule[PRICE]),
                    xbody.xpath(rule[IMAGE_URL]), xbody.xpath(rule[GOOD_URL])
            ):
                if self._extract_count >= int(self.limit):
                    break
                try:
                    items = Item()
                    items[GOOD_NAME] = "".join([des.strip() for des in good_name.xpath('text()')])
                    items[PRICE] = price
                    items[IMAGE_URL] = image_url
                    items[GOOD_URL] = good_url
                    items['cate'] = cate
                    items['shopid'] = self.kwargs.get("shopid", 1)
                except:
                    search_logger.error("Keywords ERROR")
                else:
                    self._itemlist.append(items)
                    self._extract_count += 1

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = dict((key, value.strip()) for key, value in items.items() if hasattr(value, "strip"))
            str_items[PRICE] = handler_price(str_items[PRICE])
            str_items[IMAGE_URL] = str_items[IMAGE_URL].replace('n9', 'n7', 1)
            str_items[GOOD_URL] = self.parse_phone_url(str_items[GOOD_URL])
            search_logger.debug("item is {0}".format((items,)))
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL], items['cate']])
        return itemlist

    def parse_phone_url(self, url):
        baseurl = r"http://item.m.jd.com/ware/view.action?wareId=%s"
        parse_str = urlparse.urlparse(url)
        try:
            query = parse_str.query
            pid = urlparse.parse_qs(query)['wareId'][0]
        except:
            pid = get_number(parse_str.path)
        return baseurl % pid

    def get_cate(self, xbody):
        name = xbody.xpath("//div[@class='item fore hover']/h3//a//text()")
        if name:
            return name[0]
        else:
            return ""

