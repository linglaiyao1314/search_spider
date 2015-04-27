# coding=utf-8
from engin.main import bdcrawl
import json
from flask import Flask, request
from engin.logs import search_logger

app = Flask(__name__)
app.debug = False

HEADERS = {}


@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=["POST", 'GET'])
def json_result():
    search_logger.info(".........START to ..........Search...................\n")
    if request.method == 'GET' or request.method == "POST":
        keywords = request.args.get("keywords", None)
        count = request.args.get("count", 1)
        types = request.args.get("type", None)
        shop = request.args.get("shop", "all")
        result = bdcrawl(keywords, count=count, types=types, headers=HEADERS, shop=shop)
        if result:
            search_logger.debug("Request is : %s" % result)
        else:
            search_logger.debug("Result is []")
        search_logger.info("...............Finish  This Search Session and wait for next .........\n\n")
        return json.dumps(result)


if __name__ == '__main__':
    # app.run("0.0.0.0", 8888)
    app.run()
