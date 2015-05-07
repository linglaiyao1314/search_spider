from engin.Spider import SearchSpider, Item
from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL
from engin.filter_help import *
import json


class SunSpider(SearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(SunSpider, self).__init__(name, start_urls, rule, **kwargs)

    def parse_item(self):
        for resp in self.make_request():
            goods = json.loads(resp.content)['goods']
            for element in goods:
                if self._extract_count >= int(self.limit):
                    break
                items = Item(shopid=self.kwargs.get("shopid", 8))
                items[GOOD_NAME] = element['catentdesc']
                items[PRICE] = element['price']
                items[IMAGE_URL] = r"http://image"+element['articlePoint']+r".suning.cn/b2c/catentries/"+r"000000000"+\
                                   element['partnumber']+r"_1_160x160.jpg"
                items[GOOD_URL] = r"http://m.suning.com/product/" + element['partnumber'] + ".html"
                self._extract_count += 1
                self._itemlist.append(items)

    def format_item(self):
        itemlist = []
        for items in self.get_itemlist():
            str_items = {key: value.strip() for key, value in items.items() if hasattr(value, "strip")}
            itemlist.append([items['shopid'], str_items[GOOD_NAME], str_items[PRICE],
                             str_items[IMAGE_URL], str_items[GOOD_URL]])
        return itemlist