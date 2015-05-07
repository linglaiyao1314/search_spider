from engin.Spider import CommandSearchSpider, Item
from engin.logs import search_logger
from engin.setting import *
import os
import urlparse


class PcomeSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(PcomeSpider, self).__init__(name, start_urls, rule, **kwargs)

    def parse_item(self):
        rule = self._rule["RuleOfItem"]
        for resp in self.make_request():
            search_logger.info("Spider is [ %s ]" % self._name)
            jsonbody = resp.json()
            if not jsonbody.get("prods", None):
                return
            for product in jsonbody["prods"]:
                if self._extract_count >= int(self.limit):
                    break
                try:
                    items = Item(shopid=self.kwargs.get("shopid", 30))
                    items[GOOD_NAME] = product['name']
                    items[PRICE] = str(product['price'])
                    items[IMAGE_URL] = urlparse.urljoin("http://ec1img.pchome.com.tw/", product['picS'])
                    items[GOOD_URL] = os.path.join("http://24h.pchome.com.tw/prod/", product['Id'])
                    search_logger.info("%s crawler item" % self._name)
                    search_logger.info(items)
                except:
                    search_logger.error("items crawl wrong....from %s" % self._name, exc_info=True)
                else:
                    self._itemlist.append(items)
                    self._extract_count += 1

    def format_item(self):
        return super(PcomeSpider, self).format_item()