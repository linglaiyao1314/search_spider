from engin.Spider import CommandSearchSpider


class AmaSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(AmaSpider, self).__init__(name, start_urls, rule, **kwargs)
