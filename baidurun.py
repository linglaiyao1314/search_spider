# coding=utf-8
from engin.main import bdcrawl
import json
from flask import Flask, request
app = Flask(__name__)
app.debug = True

HEADERS = {}
HEADERS_ = {"user-agent":
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"}


@app.route('/', methods=['POST', 'GET'])
@app.route('/index/', methods=["POST", 'GET'])
def json_result():
    print ".........START to ..........search..................."
    print request.method
    if request.method == 'GET' or request.method == "POST":
        keywords = request.args.get("keywords", None)
        count = request.args.get("count", 1)
        types = request.args.get("type", None)
        shop = request.args.get("shop", "all")
        result = bdcrawl(keywords, count=count, types=types, headers=HEADERS, shop=shop)
        return json.dumps(result)
    print "...............Finish ................."

if __name__ == '__main__':
    app.run()
