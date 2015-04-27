from engin.setting import GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL
from engin.filter_help import *
from engin.Spider import SearchSpider, Item
import json


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
