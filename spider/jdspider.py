# coding=utf-8
from engin.Spider import SearchSpider, Url, Item
from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL
from engin.filter_help import *
import urlparse
import json
import requests
import base64


def init_start_urls(purl, rule, **kwargs):
    url_setting = rule.get(purl, None)
    if not url_setting:
        return purl
    new_url = Url(purl)
    for parmater, value in url_setting.items():
        new_url.set_url_with_parmater(parmater, value)
    if kwargs.get("addpath", None):
        new_url.add_path(kwargs['addpath'])
    return new_url.get_usual_url()


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


class SunSpider(SearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(SunSpider, self).__init__(name, start_urls, rule, **kwargs)

    def parse_item(self, limit):
        for resp in self.make_request():
            show_state("Spider is ->", self._name)
            goods = json.loads(resp.content)['goods']
            for element in goods:
                if self._extract_count >= int(limit):
                    break
                items = Item(shopid=self.kwargs.get("shopid", 8))
                items[GOOD_NAME] = element['catentdesc']
                items[PRICE] = element['price']
                items[IMAGE_URL] = r"http://image"+element['articlePoint']+r".suning.cn/b2c/catentries/"+r"000000000"+\
                                   element['partnumber']+r"_1_160x160.jpg"
                items[GOOD_URL] = r"http://m.suning.com/product/" + element['partnumber'] + ".html"
                show_state("%s crawler item" % self._name, items)
                self._extract_count += 1
                self._itemlist.append(items)

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist


class TmSpider(SearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(TmSpider, self).__init__(name, start_urls, rule, **kwargs)

    def parse_item(self, limit):
        for resp in self.make_request():
            show_state("Spider is ->", self._name)
            goods = json.loads(resp.content)['listItem']
            for element in goods:
                if self._extract_count >= int(limit):
                    break
                items = Item(shopid=self.kwargs.get("shopid", 4))
                items[GOOD_NAME] = element['title_small']
                items[PRICE] = element['price'] if not element['mobile_price'].strip() else element['mobile_price']
                items[IMAGE_URL] = element['img']
                items[GOOD_URL] = element['url']
                show_state("%s crawler item" % self._name, items)
                self._itemlist.append(items)
                self._extract_count += 1

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist


class JdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(JdSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.pattern = r'{"available.*?}'

    def get_all(self, body):
        return re.findall(self.pattern, body)

    def parse_item(self, limit):
        for resp in self.make_request():
            show_state("Spider is ->", self._name)
            goods = self.get_all(resp.content)
            for element in goods:
                if self._extract_count >= int(limit):
                    break
                element = json.loads(element)
                items = Item(shopid=self.kwargs.get("shopid", 1))
                items[GOOD_NAME] = element['wname']
                items[PRICE] = element['jdPrice']
                items[IMAGE_URL] = element['imageurl']
                items[GOOD_URL] = "http://item.m.jd.com/ware/view.action?wareId=%s&region=" % element['wareId']
                show_state("%s crawler item" % self._name, items)
                self._itemlist.append(items)
                self._extract_count += 1

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            str_items[PRICE] = handler_price(str_items[PRICE])
            str_items[IMAGE_URL] = str_items[IMAGE_URL].replace('n4', 'n7', 1)
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist


class BdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(BdSpider, self).__init__(name, start_urls, rule, **kwargs)

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
                    items = Item()
                    items[GOOD_NAME] = good_name
                    items[PRICE] = self.parse_price(price)
                    items[IMAGE_URL] = image_url
                    good_url = urlparse.urljoin(self.kwargs['domain'], good_url)
                    with request_open(requests.get(good_url)) as r:
                        good_url = r.url
                    items[GOOD_URL] = good_url
                    show_state("%s crawler item" % self._name, items)
                except:
                    show_state("Keywords ERROR", "items crawl wrong....")
                else:
                    self._itemlist.append(items)
                    self._extract_count += 1

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            str_items[PRICE] = handler_price(str_items[PRICE])
            items["shopid"] = self.parse_shopid(str_items[GOOD_URL])
            str_items[GOOD_URL] = self.converse_url(items['shopid'], str_items[GOOD_URL])
            str_items[IMAGE_URL] = self.converse_img_url(str_items[IMAGE_URL])
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist

    def parse_price(self, price_xpath):
        b_tag = price_xpath.xpath('b/text()')
        if b_tag:
            pint = b_tag[0]
            pdec = get_dot_number("".join(price_xpath.xpath('text()')))
            return pint + pdec
        else:
            return price_xpath.xpath('text()')[0]

    def parse_shopid(self, purl):
        if purl.find("jd.com") > 0:
            return 1
        elif purl.find("suning.com") > 0:
            return 8
        elif purl.find("tmall.com") > 0:
            return 4
        elif purl.find("amazon") > 0:
            return 7
        elif purl.find("yhd.com") > 0:
            return 3
        elif purl.find("dangdang") > 0:
            return 5
        else:
            return 19

    def parse_query_productid(self, purl):
        try:
            dct = urlparse.parse_qs(purl)
        except:
            return purl
        else:
            return dct['product_url'][0]

    @exception
    def converse_url(self, shopid, purl):
        if shopid == 1:
            head = "http://item.m.jd.com/ware/view.action?wareId="
            tail = str(get_number(urlparse.urlparse(purl).path))
            return head + tail
        elif shopid == 8:
            head = "http://m.suning.com/product/%s.html"
            tail = str(get_number(urlparse.urlparse(purl).path))
            return head % tail
        elif shopid == 5:
            head = "http://m.dangdang.com/product.php?pid=%s"
            purl = self.parse_query_productid(purl)
            dct = urlparse.parse_qs(purl)
            tail = str(get_number(dct['backurl'][0]))
            return head % tail
        elif shopid == 7:
            purl = self.parse_query_productid(purl)
            return purl
        elif shopid == 3:
            head = "http://item.m.yhd.com/item/%s"
            purl = self.parse_query_productid(purl)
            tail = get_number(urlparse.urlparse(purl).path)
            return head % tail
        else:
            return purl

    def converse_img_url(self, purl):
        return base64.encodestring(purl)


class DangDangSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(DangDangSpider, self).__init__(name, start_urls, rule, **kwargs)


class YhdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(YhdSpider, self).__init__(name, start_urls, rule, **kwargs)


class AmaSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(AmaSpider, self).__init__(name, start_urls, rule, **kwargs)

