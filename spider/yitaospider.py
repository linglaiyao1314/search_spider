from engin.Spider import CommandSearchSpider


class YiTaoSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(YiTaoSpider, self).__init__(name, start_urls, rule, **kwargs)

    def format_item(self):
        itemlist = super(YiTaoSpider, self).format_item()
        if itemlist:
            for item in itemlist:
                item.append("")
        return itemlist

