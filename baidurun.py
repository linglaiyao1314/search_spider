# coding=utf-8
from engin.main import bdcrawl, momocrawl, pinglecrawl, yitaocrawl
import json
from flask import Flask, request
from engin.logs import search_logger, INFO, DEBUG, ERROR, wrapstring

app = Flask(__name__)
app.debug = False


# HEADERS = {"User-Agent":
# "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko)Chrome/38.0.2125.122 Safari/537.36"}
HEADERS = {"User-Agent":
               "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:39.0) Gecko/20100101 Firefox/39.0"}


def activity_api(itemlist):
    for item in itemlist:
        if u"图书" in item[-1]:
            item[-1] = u"图书"
    return itemlist


def convert_resut(results):
    """
    对返回结果的格式进行修正
    """
    if not results:
        return []
    return [{'sid': i[0],
             'product_name': i[1],
             'price': i[2],
             'img': i[3],
             'url': i[4],
             'cate': i[5], } for i in results]


@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=["POST", 'GET'])
def json_result():
    search_logger.info(".........START to ..........Search...................\n")
    keywords, country_id = ("", 1)
    if request.method == 'POST':
        keywords = request.form.get("keywords", "")
        country_id = int(request.form.get("country_id", 1))
    elif request.method == 'GET':
        keywords = request.args.get("keywords", None)
        country_id = int(request.args.get("country_id", 1))
    search_logger.info(wrapstring("Keywords is : [ %s ]" % keywords))
    if country_id == 1:
        result = bdcrawl(keywords, headers=HEADERS)
    elif country_id == 2:
        result = pinglecrawl(keywords, headers=HEADERS)
        if not result:
            search_logger.info(wrapstring("Pingle have no result, so go to momo and pchome...."))
            result = momocrawl(keywords, headers=HEADERS)
            # result = momo_pc_event(keywords, headers=HEADERS, shop=shop)
    else:
        result = []
    search_logger.debug(wrapstring("There %d items will be return\n\n" % len(result), DEBUG))
    result = activity_api(result)
    return json.dumps(convert_resut(result))


if __name__ == '__main__':
    # app.run("0.0.0.0", 8888)
    app.run()
