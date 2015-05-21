from engin.Spider import CommandSearchSpider


class PingleSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(PingleSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.kwargs["timeout"] = 10

    def format_item(self):
        itemlist = super(PingleSpider, self).format_item()
        if itemlist:
            for item in itemlist:
                item.append("")
            return itemlist

