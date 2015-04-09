# coding=utf-8
from engin.main import crawl
import json
from flask import Flask, request
app = Flask(__name__)
app.debug = False

HEADERS = {}
HEADERS_ = {"user-agent":
               "Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/38.0.2125.122 Safari/537.36"}
@app.route('/')
@app.route('/index/')
def json_result():
    print ".........START to ..........search..................."
    keywords = request.args.get("keyword", None)
    count = request.args.get("count", 1)
    types = request.get_data("type", None)
    result = crawl(keywords, count=count, types=types, headers=HEADERS)
    # result = crawl(keywords, count=count, types=types, headers=HEADERS_)
    print "...............RETURN the result ................."
    return json.dumps(result)


if __name__ == '__main__':
    app.run()
