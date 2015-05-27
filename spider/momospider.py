from engin.Spider import CommandSearchSpider


class MomoSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(MomoSpider, self).__init__(name, start_urls, rule, **kwargs)
        self.kwargs["timeout"] = 5

    def format_item(self):
        itemlist = super(MomoSpider, self).format_item()
        if itemlist:
            for item in itemlist:
                item.append("")
        return itemlist