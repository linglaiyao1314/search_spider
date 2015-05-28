# coding=utf-8
__author__ = 'user'
import logging

INFO = logging.INFO
DEBUG = logging.DEBUG
ERROR = logging.ERROR

COLOR = {
    INFO: '\033[92m',  # 绿
    ERROR: '\033[91m',  # 红
    DEBUG: '\033[94m',  # 蓝
    "end": "\33[0m"
}


# 打印上色
def wrapstring(string, level=INFO):
    return COLOR[level] + string + COLOR["end"]

formatter = logging.Formatter('%(asctime)s - %(filename)s[line:%(lineno)d] - %(levelname)s - %(message)s')
search_logger = logging.getLogger("search_loger")
search_logger.setLevel(logging.DEBUG)
search_file_handler = logging.FileHandler(r"search_loger.log")
search_screen_handler = logging.StreamHandler()
search_file_handler.setLevel(logging.DEBUG)
search_screen_handler.setLevel(logging.DEBUG)
search_file_handler.setFormatter(formatter)
search_screen_handler.setFormatter(formatter)
search_logger.addHandler(search_file_handler)
search_logger.addHandler(search_screen_handler)


# img_logger = logging.getLogger("img_logger")
# img_logger.setLevel(logging.DEBUG)
# img_file_handler = logging.FileHandler("img_loger.log")
# img_screen_handler = logging.StreamHandler()
# img_file_handler.setLevel(logging.DEBUG)
# img_screen_handler.setLevel(logging.DEBUG)
# img_file_handler.setFormatter(formatter)
# img_screen_handler.setFormatter(formatter)
# img_logger.addHandler(img_file_handler)
# img_logger.addHandler(img_screen_handler)