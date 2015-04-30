# coding=utf-8
import threading
from spider.jdspider import JdSpider, JdSpiderPc
from Spider import Url
from setting import URL_RULE, SEARCH_RULE
import urllib
from spider.bdwgpider import BdSpider
from logs import search_logger


def init_start_urls(url, rule, **kwargs):
    url_setting = rule.get(url, None)
    if not url_setting and not kwargs:
        return url
    new_url = Url(url)
    for parmater, value in url_setting.items():
        new_url.set_url_with_parmater(parmater, value)

    if kwargs.get("path", None):
        new_url.set_url_with_parmater("path", kwargs['path'])
    if kwargs.get("addpath", None):
        new_url.add_path(kwargs['addpath'])
    return new_url.get_usual_url()


class RunSpiderThread(threading.Thread):
    def __init__(self, spider, count):
        threading.Thread.__init__(self)
        self.spider = spider
        self.res = []
        self.count = count

    def run(self):
        self.spider.parse_item(limit=self.count)
        self.res = self.spider.format_item()

    def getresult(self):
        return self.res


def main(spiders, count):
    itemlist = []
    threads = []
    for spider in spiders:
        t = RunSpiderThread(spider, count)
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
    for thread in threads:
        itemlist.extend(thread.getresult())
    return itemlist


def crawl(search="Kindle", **kwargs):
    headers = kwargs.get("headers")
    testurl = init_start_urls("http://m.jd.com/", URL_RULE)
    shspider = JdSpider("jd", testurl, SEARCH_RULE, params={"keyword": search}, shopid=1, headers=headers)

    # testdd = init_start_urls("http://m.dangdang.com/", URL_RULE)
    # ddspider = DangDangSpider("dangdang", testdd, SEARCH_RULE, params={"key": search}, shopid=5, headers=headers)
    #
    # testyhd = init_start_urls("http://search.m.yhd.com/", URL_RULE, addpath="k"+search)
    # yhdspider = YhdSpider("yhd", testyhd, SEARCH_RULE, shopid=3, headers=headers)
    #
    # testama = init_start_urls("http://www.amazon.cn/", URL_RULE)
    # amaspider = AmaSpider("ama", testama, SEARCH_RULE, shopid=7, params={"ref": "is_box_", "k": search}, headers=headers)
    #
    # # http://search.suning.com/emall/mobile/mobileSearch.jsonp?cityId=9173&keyword=%E6%89%8B%E6%9C%BA&set=5
    # testsun = init_start_urls("http://search.suning.com/emall/mobile/mobileSearch.jsonp", URL_RULE)
    # sunspider = SunSpider("sun", testsun, SEARCH_RULE, shopid=8,
    #                       params={"cityId": "9173", "keyword": search, "set": 5}, headers=headers)
    #
    # # http://s.m.tmall.com/m/search_data.htm?p=1&q=%CA%D6%BB%FA
    # testtm = init_start_urls("http://s.m.tmall.com/m/search_data.htm?p=1&q=" + urllib.quote(search.encode('gbk')),
    #                          URL_RULE)
    # tmspider = TmSpider("tm", testtm, SEARCH_RULE, shopid=4, header=headers)
    #
    # count = kwargs.get("count", 1)
    # shop = kwargs.get("shop", "all")
    #
    # spiders_dict = {
    #     u"1": shspider, u"5": ddspider, u"3": yhdspider, u"7": amaspider, u"8": sunspider, u"4": tmspider
    # }
    # if shop == "all":
    #     return main([shspider, ddspider, amaspider, yhdspider, sunspider, tmspider], count)
    # else:
    #     spiders = []
    #     for i in shop.split(","):
    #         spiders.append(spiders_dict.get(i, None))
    #     spiders = [s for s in spiders if s is not None]
    #     assert len(spiders) != 0, "Can't find these shopid"
    #     return main(spiders, count)


def bdcrawl(search="Kindle", **kwargs):
    headers = kwargs.get("headers")
    bdurl = init_start_urls("http://weigou.baidu.com/", URL_RULE)
    bdspider = BdSpider("bd", bdurl, SEARCH_RULE, params={"q": search},
                        headers=headers, domain="http://weigou.baidu.com/")
    bdspider.parse_item(limit=5)
    result = bdspider.format_item()
    if result:
        return result
    else:
        search_logger.info("baidu weigou is empty, so go to JD ")
        # testurl = init_start_urls("http://m.jd.com/", URL_RULE)
        testurl = "http://search.jd.com/Search?keyword=%E7%BA%A2%E7%90%83&enc=utf-8"
        shspider = JdSpiderPc("jdpc", testurl, SEARCH_RULE, params={"keyword": search}, shopid=1, headers=headers)
        return main([shspider], 5)


if __name__ == '__main__':
    bdcrawl()