# coding=utf-8
import re
import time
from contextlib import contextmanager
# from w3lib.html import remove_tags
from logs import search_logger


# 过滤出字符串的中文
def get_chinese(s):
    pattren = re.compile(u"[\u4e00-\u9fa5]")    # 匹配一个中文字符,注意正则表达式必须前面+u
    return filter(lambda x: re.match(pattren, x), s)


# 过滤非字符串的非中文
def get_others(s):
    pattern = re.compile(u"[^\u4e00-\u9fa5]")
    return filter(lambda x: re.match(pattern, x), s)


# 过滤字符串的数字
def get_number(s):
    pattern = re.compile(u"[\d]")
    return filter(lambda x: re.match(pattern, x), s)


def get_dot_number(s):
    pattern = re.compile(u"[\d\.]")
    return filter(lambda x: re.match(pattern, x), s)


def handler_price(price):
    """
    专用于处理形如xx.xx的价格， 过滤出price中的数字
    :param price 价格字符串
    """
    if price.find(".") < 0:
        return get_number(price)
    else:
        head, tail = price.split(".")
        return "".join([get_number(head), ".", get_number(tail)])


@contextmanager
def request_open(thing, errmsg="error"):
    """
    url 请求上下文管理器
    """
    try:
        yield thing
    except:
        search_logger.error("%s" % errmsg)
    finally:
        thing.close()


@contextmanager
def timer(func, errmsg="err"):
    """
    统计函数运行时间
    """
    start = time.time()
    try:
        yield func
    except:
        print errmsg
    finally:
        end = (time.time() - start) * 1000
        print "cost time: %.3f seconds" % end


def parse_query_productid(url):
    import urlparse
    dct = urlparse.parse_qs(url)
    return dct['product_url'][0]


def exception(func):
    """异常处理装饰器"""
    def _wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except:
            pass
        else:
            return result
    return _wrap


