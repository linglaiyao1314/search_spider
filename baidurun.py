# coding=utf-8
from engin.main import bdcrawl
from momo import momocrawl
import json
from flask import Flask, request
from engin.logs import search_logger

app = Flask(__name__)
app.debug = False

HEADERS = {}


def activity_api(itemlist):
    for item in itemlist:
        if u"图书" in item[-1]:
            item[-1] = u"图书"
    return itemlist


@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=["POST", 'GET'])
def json_result():
    search_logger.info(".........START to ..........Search...................\n")
    if request.method == 'GET' or request.method == "POST":
        keywords = request.args.get("keywords", None)
        count = request.args.get("count", 1)
        types = request.args.get("type", None)
        shop = request.args.get("shop", "all")
        country_id = request.args.get("country_id",1)
        search_logger.info("Keywords is : [ %s ]" % keywords)
        if int(country_id) == 1:
            result = bdcrawl(keywords, count=count, types=types, headers=HEADERS, shop=shop)
        elif int(country_id) == 2:
            try:
                result = momocrawl(keywords)
            except Exception,e:
                search_logger.error(e,exc_info=1)
                result = []
        result = json.dumps(activity_api(result))
        search_logger.debug("RETURN:%s"%result)
        #search_logger.info("...............Finish  This Search Session and wait for next .........\n\n")
        return result


if __name__ == '__main__':
    app.run("0.0.0.0", 8888)
