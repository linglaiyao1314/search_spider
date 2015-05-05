from engin.Spider import CommandSearchSpider


class MomoSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(MomoSpider, self).__init__(name, start_urls, rule, **kwargs)

    def format_item(self):
        return super(MomoSpider, self).format_item()