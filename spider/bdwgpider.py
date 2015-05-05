# coding=utf-8
from engin.Spider import CommandSearchSpider, Item
from engin.setting import *
import urlparse
from engin.filter_help import *
import requests
import base64
import json
from engin.logs import search_logger


class BdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(BdSpider, self).__init__(name, start_urls, rule, **kwargs)

    def parse_item(self, limit):
        rule = self._rule["RuleOfItem"]
        for resp in self.make_request():
            xbody = self.get_html_body_by_lxml(resp)
            cate = self.get_cate(xbody)
            search_logger.info("request for cate....and cate is [ %s ]" % cate)
            search_logger.info("request for items in [ 百度微购 ]")
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
                    items['cate'] = cate
                    search_logger.debug("item is %s" % items)
                except:
                    search_logger.error("Keywords ERROR")
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
                             str_items[IMAGE_URL], str_items[GOOD_URL], items['cate']])
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
            return 24

    def parse_query_productid(self, purl):
        try:
            dct = urlparse.parse_qs(purl)
        except:
            return purl
        else:
            try:
                result = dct['product_url'][0]
            except:
                result = dct['to'][0]
            return result

    @exception
    def converse_url(self, shopid, purl):
        if shopid == 1:
            head = "http://item.m.jd.com/ware/view.action?wareId="
            tail = str(get_number(urlparse.urlparse(purl).path))
            if not tail:
                purl = self.parse_query_productid(purl)
                tail = get_number(urlparse.urlparse(purl).path)
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

    def converse_img_url(self, purl, baseurl="http://query.viscovery.net.cn/hrs_img.php?img_url="):
        img_url = base64.encodestring(purl)
        return baseurl + img_url

    def get_cate(self, xbody):
        try:
            content = xbody.xpath("//div[@id='raw-category']//text()")[0]
            result = json.loads(content.replace("&quot;", '"'))
            name = result["sub_cat"][0]['sub_cat'][0]["name"]
        except:
            return
        else:
            return name

