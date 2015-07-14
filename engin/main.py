# coding=utf-8
import threading
from spider.jdspider import JdSpider, JdSpiderPc
from spider.momospider import MomoSpider
from spider.pcomespider import PcomeSpider
from spider.pinglespider import PingleSpider
from spider.yitaospider import YiTaoSpider
from Spider import Url
from setting import URL_RULE, SEARCH_RULE
from spider.bdwgpider import BdSpider
from logs import search_logger, INFO, ERROR, DEBUG, wrapstring
import urllib2
import random
import urllib
from traceback import print_exc


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
    def __init__(self, spider):
        threading.Thread.__init__(self)
        self.spider = spider
        self.res = []

    def run(self):
        try:
            self.spider.parse_item()
        except Exception, e:
            search_logger.error(wrapstring("[%s] error-%s" % (self.spider._name, e), ERROR))
            self.res = []
        else:
            self.res = self.spider.format_item()

    def getresult(self):
        return self.res


def main(spiders):
    itemlist = []
    threads = []
    for spider in spiders:
        t = RunSpiderThread(spider)
        threads.append(t)
    for thread in threads:
        thread.start()
    for thread in threads:
        thread.join(timeout=5)
    for thread in threads:
        itemlist.extend(thread.getresult())
    samples = 5 if len(itemlist) >= 5 else len(itemlist)
    random.shuffle(itemlist)
    return random.sample(itemlist, samples)


# 先搜百度微购，没结果则再搜京东
def bdcrawl(search="Kindle", **kwargs):
    headers = kwargs.get("headers")
    bdurl = init_start_urls("http://weigou.baidu.com/", URL_RULE)
    # 按人气排序
    bdspider = BdSpider("bd", bdurl, SEARCH_RULE, params={"q": search, "sort_type": "comment_num_desc"},
                        headers=headers, domain="http://weigou.baidu.com/", timeout=5)
    try:
        bdspider.parse_item()
    except Exception, e:
        search_logger.error(wrapstring("[baiduweigou] error->%s" % e, ERROR))
        result = []
    else:
        result = bdspider.format_item()
    if result:
        return result
    else:
        search_logger.info("baidu weigou is empty, so go to JingDong shop......")
        # testurl = init_start_urls("http://m.jd.com/", URL_RULE)
        testurl = "http://search.jd.com/Search?keyword=%E7%BA%A2%E7%90%83&enc=utf-8"
        shspider = JdSpiderPc("jdpc", testurl, SEARCH_RULE, params={"keyword": search},
                              shopid=1, headers=headers, timeout=5)
        return main([shspider])


# momo爬虫
def momocrawl(search='Kindle', **kwargs):
    headers = kwargs.get("headers")
    url = "http://www.momoshop.com.tw/mosearch/%s.html" % urllib2.quote(search.encode('utf-8'))
    momospider = MomoSpider("momo", url, SEARCH_RULE, params={"keyword": search},
                            shopid=27, headers=headers, timeout=7, limit=5)
    pcurl = "http://ecshweb.pchome.com.tw/search/v3.3/all/results"
    pcomespider = PcomeSpider("pcome", pcurl, SEARCH_RULE, params={"q": search},
                              shopid=30, headers=headers, timeout=7, limit=5)
    return main([momospider, pcomespider])


# 品购
def pinglecrawl(search="Kindle", **kwargs):
    headers = kwargs.get("headers")
    keywords = urllib.quote(search.encode("utf8"))
    pgurl = "http://www.pingle.com.tw/q/%s" % keywords
    try:
        pinglespider = PingleSpider("pingle", pgurl, SEARCH_RULE, shopid=33, headers=headers, timeout=5, limit=5)
        pinglespider.parse_item()
    except Exception, e:
        search_logger.error(wrapstring("[pingle] error->%s" % e, ERROR))
        return []
    else:
        return pinglespider.format_item()


# 一淘网
def yitaocrawl(search="Kindle", **kwargs):
    headers = kwargs.get("headers")
    keywords = search
    pgurl = "http://s.etao.com/search?q=%s" % keywords
    try:
        yitaospider = YiTaoSpider("yitao", pgurl, SEARCH_RULE, shopid=999, headers=headers, timeout=5, limit=5)
        yitaospider.parse_item()
    except Exception, e:
        print print_exc()
        search_logger.error(wrapstring("[yitao] error->%s" % e, ERROR))
        return []
    else:
        return yitaospider.format_item()