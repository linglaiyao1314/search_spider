from engin.Spider import CommandSearchSpider
import urllib
from engin.Spider import *


class PingleSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(PingleSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.kwargs["timeout"] = 10

    def parse_item(self):
        rule = self._rule["RuleOfItem"]
        for resp in self.make_request():
            search_logger.info(wrapstring("Spider is [ %s ]" % self._name))
            xbody = self.get_html_body_by_lxml(resp)
            if xbody.xpath("//div[@class='Oops']"):
                search_logger.error(wrapstring("can't find these goods", level=DEBUG))
                break
            for good_name, price, image_url, good_url in zip(
                    xbody.xpath(rule[GOOD_NAME]), xbody.xpath(rule[PRICE]),
                    xbody.xpath(rule[IMAGE_URL]), xbody.xpath(rule[GOOD_URL])
            ):
                if self._extract_count >= int(self.limit):
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
                    search_logger.error(wrapstring("items crawl wrong....from %s" % self._name, True), exc_info=True)
                else:
                    self._itemlist.append(items)
                    self._extract_count += 1

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = dict((key, value.strip()) for key, value in items.items() if hasattr(value, "strip"))
            str_items[PRICE] = handler_price(str_items[PRICE])
            str_items[IMAGE_URL] = urlparse.urljoin(self._rule['domain'], str_items[IMAGE_URL])
            newshopid = self.parse_shopid(self.parse_url_with_shopid(str_items[GOOD_URL])) or items["shopid"]
            itemlist.append([newshopid, str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist

    def parse_url_with_shopid(self, url):
        new_url = urllib.unquote(url)
        return urllib.splitvalue(new_url)[1]

    def parse_shopid(self, url):
        if url.find("momoshop") > 0:
            return 27
        elif url.find("yahoo") > 0:
            return 25
        elif url.find(".udn.") > 0:
            return 38
        elif url.find("pchome") > 0:
            return 30
        else:
            return

