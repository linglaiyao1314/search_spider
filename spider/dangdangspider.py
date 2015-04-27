from engin.Spider import CommandSearchSpider


class DangDangSpider(CommandSearchSpider):
    def __init__(self, name, start_urls, rule, **kwargs):
        super(DangDangSpider, self).__init__(name, start_urls, rule, **kwargs)
