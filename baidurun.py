# coding=utf-8
from engin.main import bdcrawl
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
        search_logger.info("Keywords is : [ %s ]" % keywords)
        result = bdcrawl(keywords, count=count, types=types, headers=HEADERS, shop=shop)
        search_logger.debug("There %d items will be return" % len(result))
        search_logger.info("...............Finish  This Search Session and wait for next .........\n\n")
        return json.dumps(activity_api(result))


if __name__ == '__main__':
    app.run("0.0.0.0", 8888)
    # app.run()
