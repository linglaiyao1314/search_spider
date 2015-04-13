# coding=utf-8
from engin.main import bdcrawl
import json
from flask import Flask, request
app = Flask(__name__)
app.debug = False

HEADERS = {}


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
    app.run("0.0.0.0", 8888)
