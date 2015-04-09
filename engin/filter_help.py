# coding=utf-8
import re
import time
from PIL import Image
import pytesseract
from StringIO import StringIO
import requests

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


def filter_num_from_img_by_requests(imgurl):
    try:
        r = requests.get(imgurl, timeout=5)
        img = Image.open(StringIO(r.content))
        result = pytesseract.image_to_string(img)
    except:
        return None
    else:
        return result


def filter_num_from_img(imgpath):
    try:
        img = Image.open(imgpath)
        result = pytesseract.image_to_string(img)
    except:
        return None
    else:
        return result


if __name__ == '__main__':
    print get_chinese(u"2013:13:12这csac是45615中vxz文")
    print get_others(u"2013:13:12这cxz是45615中vcx文")
    print get_number(u"$12.00")
    print filter_num_from_img_by_requests("http://price2.suning.cn/webapp/wcs/stores/prdprice/24190224_9173_10000_9-1.png")
    print filter_num_from_img(r"C:\Users\admin\Downloads\bootstrap-3.3.4-dist\1.png")
