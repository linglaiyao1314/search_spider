# coding=utf-8
import re
import time
from contextlib import contextmanager


CH = re.compile(u"[\u4e00-\u9fa5]")  # 匹配一个中文字符,注意正则表达式必须前面+u


# 过滤出字符串的中文
def get_chinese(s):
    pattren = re.compile(u"[\u4e00-\u9fa5]")
    return filter(lambda x: re.match(pattren, x), s)


def get_others(s):
    pattern = re.compile(u"[^\u4e00-\u9fa5]")
    return filter(lambda x: re.match(pattern, x), s)


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
        return "".join([get_number(head), ".", tail])


def show_state(key, value):
    now = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time()))
    print
    print "[", now, "]:", key, value
    print


@contextmanager
def request_open(thing, errmsg="error"):
    try:
        yield thing
    except:
        print "%s" % errmsg
    finally:
        thing.close()


@contextmanager
def timer(func, errmsg="err"):
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
    def _wrap(*args, **kwargs):
        try:
            result = func(*args, **kwargs)
        except:
            pass
        else:
            return result
    return _wrap


if __name__ == '__main__':
    print get_chinese(u"2013:13:12这csac是45615中vxz文")
    print get_others(u"2013:13:12这cxz是45615中vcx文")
    print get_number(u"$12.00")
    url = parse_query_productid(
        "http://weigou.baidu.com/site/transition?pid=232011642&merchant_name=1%E5%8F%B7%E5%BA%97&product_url=http%3A%2F%2Fitem.yhd.com%2Fitem%2F12985679%3Ftracker_u%3D10778743%26union_ref%3D5%26weigou_transition_key%3D6a52f5191f75bf0bc34577f29c994c9a"
    )
    print get_dot_number(u'\xa5\r\n                    \r\n                    .40')

