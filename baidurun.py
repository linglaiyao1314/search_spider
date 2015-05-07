# coding=utf-8
from engin.main import bdcrawl, momocrawl
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
        shop = request.args.get("shop", "all")
        country_id = int(request.args.get("country_id", 1))
        search_logger.info("Keywords is : [ %s ]" % keywords)
        if country_id == 1:
            result = bdcrawl(keywords, headers=HEADERS, shop=shop)
        elif country_id == 2:
            result = momocrawl(keywords, headers=HEADERS, shop=shop)
            # result = momo_pc_event(keywords, headers=HEADERS, shop=shop)
        else:
            result = []
        search_logger.debug("There %d items will be return\n\n" % len(result))
        return json.dumps(activity_api(result))


if __name__ == '__main__':
    # app.run("0.0.0.0", 8888)
    app.run()
