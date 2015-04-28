# coding=utf-8
"""
    商家 ： ｛
        域名: ""
        配置参数：""
        xpath抓取规则:""
%s"""

GOOD_NAME, PRICE, IMAGE_URL, GOOD_URL = ("good_name", "price", "image_url", "good_url")
SEARCH_RULE = {

    "jd": {
        "domain": "http://m.jd.com/",
        "kwargs": {},
        "RuleOfItem": {
            GOOD_NAME: "//strong[@class='new-mu_l2h']//text()",
            PRICE: "//strong[@class='new-txt-rd2']//text()",
            IMAGE_URL: "//span[@class='new-mu_tmb']//img//@imgsrc",
            GOOD_URL: "//a[@class='new-mu_l2a']//@href",
        }
    },

    "jdpc": {
        "domain": "http://www.jd.com/",
        "kwargs": {},
        "RuleOfItem": {
            GOOD_NAME: "//ul[@class='list-h clearfix']//div[@class='p-name']/a",
            PRICE: "//ul[@class='list-h clearfix']//strong//@data-price",
            IMAGE_URL: "//ul[@class='list-h clearfix']//img//@data-lazyload",
            GOOD_URL: "//ul[@class='list-h clearfix']//div[@class='p-name']//a//@href",
        }
    },

    "dangdang": {
        "domain": "http://m.dangdang.com/",
        "kwargs": {},
        "RuleOfItem": {
            GOOD_NAME: "//span[@class='prouct_name']//a//text()",
            PRICE: "//p//span[3]//text()",
            IMAGE_URL: "//p//span[2]//img//@src",
            GOOD_URL: "//span[@class='prouct_name']//a//@href",
        }
    },

    "yhd": {
        "domain": "http://search.m.yhd.com/",
        "kwargs": {},
        "RuleOfItem": {
            GOOD_NAME: "//div[@class='title_box']//text()",
            PRICE: "//span[@class='new_price']//i//text()",
            IMAGE_URL: "//div[@class='pic_box']//img/@src",
            GOOD_URL: "//li[@data-tcs='SEARCH.0']//a/@href",
        }
    },

    "ama": {
        "domain": "http://www.amazon.cn/",
        "kwargs": {},
        "RuleOfItem": {
            GOOD_NAME: "//span[@class='productTitle']//a/text()",
            PRICE: "//span[@class='dpOurPrice']//text()",
            IMAGE_URL: "//tbody//td[@width]//img/@src",
            GOOD_URL: "//span[@class='productTitle']//a/@href",
        }
    },

    "sun": {
        "domain": "http://search.suning.com/emall/mobile/mobileSearch.jsonp",
        "kwargs": {},
        "RuleOfItem": {
            # GOOD_NAME: "//div[@class='inforBg']/h3/a/@title",
            # PRICE: "//img[@class='liprice']/@src2",
            # IMAGE_URL: "//img[@class='err-product']/@src2",
            # GOOD_URL: "//div[@class='proListTile']/ul//a[@class='search-bl']/@href",
        }
    },

    "tm": {
        "domain": "http://s.m.tmall.com/m/search_data.htm",
        "kwargs": {},
        "RuleOfItem": {
            # GOOD_NAME: "//div[@class='inforBg']/h3/a/@title",
            # PRICE: "//img[@class='liprice']/@src2",
            # IMAGE_URL: "//img[@class='err-product']/@src2",
            # GOOD_URL: "//div[@class='proListTile']/ul//a[@class='search-bl']/@href",
        }
    },

    "bd": {
        "domain": "http://weigou.baidu.com/",
        "kwargs": {},
        "RuleOfItem": {
            GOOD_NAME: "//div[@class='result-info']//@title",
            PRICE: "//div[@class='result-price']//span",
            IMAGE_URL: "//div[@class='result-pic']//img//@data-original",
            GOOD_URL: "//div[@class='result-pic']//a//@href",
        }
    },

}

URL_RULE = {
    "http://m.jd.com/": {"path": r"ware/search.action"},
    "http://m.dangdang.com/": {"path": r"gw_search.php"},
    "http://search.m.yhd.com/": {"path": r"/search/"},
    "http://www.amazon.cn/": {"path": r"/gp/aw/s/"},
    "http://search.suning.com/emall/mobile/mobileSearch.jsonp": {},
    "http://s.m.tmall.com/m/search_data.htm": {},
    "http://weigou.baidu.com/": {"path": r"search"},
}