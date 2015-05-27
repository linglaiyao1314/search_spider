from engin.Spider import CommandSearchSpider
import urllib


class PingleSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(PingleSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.kwargs["timeout"] = 10

    def format_item(self):
        # [shopid, name, price, imgurl, url, cate]
        itemlist = super(PingleSpider, self).format_item()
        if not itemlist:
            return []
        for item in itemlist:
            item[4] = self.parse_url_with_shopid(item[4])
            new_shopid = self.parse_shopid(item[4])
            item[0] = item[0] if not new_shopid else new_shopid
            item.append("")
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

