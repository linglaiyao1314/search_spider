from engin.Spider import CommandSearchSpider


class YhdSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(YhdSpider, self).__init__(name, start_urls, rule, **kwargs)
