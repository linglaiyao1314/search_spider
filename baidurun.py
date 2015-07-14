# coding=utf-8
from engin.main import bdcrawl, momocrawl, pinglecrawl, yitaocrawl
import json
from flask import Flask, request
from engin.logs import search_logger, INFO, DEBUG, ERROR, wrapstring


app = Flask(__name__)
app.debug = False

HEADERS = {"User-Agent":
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"}


def activity_api(itemlist):
    for item in itemlist:
        if u"图书" in item[-1]:
            item[-1] = u"图书"
    return itemlist


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
    return json.dumps(activity_api(result))


if __name__ == '__main__':
    app.run("0.0.0.0", 8888)
    # app.run()
