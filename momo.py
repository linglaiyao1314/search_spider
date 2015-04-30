# -*- coding:utf-8 -*-
import urllib2
from bs4 import BeautifulSoup as bs
import re
import urllib

def momocrawl(keywords, count=5):
	url = "http://www.momoshop.com.tw/mosearch/%s.html" % urllib2.quote(keywords.encode('utf-8'))
	print 'momo url:',url
	req = urllib2.Request(url,headers={ "User-agent":"Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/41.0.2272.89 Safari/537.36" ,"Referer":'www.momoshop.com.tw'})
	html = urllib2.urlopen(req).read()
	#print html
	#html = re.findall(ur'<div id="searchResults">(.*?)</div>',html.decode('utf-8','ignore'))
	soup = bs(html,"html5lib")
	#print soup
	all_product_tag = soup.find("div",attrs={"id":"searchResults"})
	#print all_product_tag
	li_tag = bs(str(all_product_tag)).find_all("li")
	result = []
	#print li_tag
	for li in li_tag:
		one = [27]
		goods_name_tags = li.find("span",attrs={"id":"goods_name"})
		if not goods_name_tags:
			goods_name_tags = li.find("p",attrs={"id":"goods_name"})
		one.append(goods_name_tags.a.text.strip())
		price_tag = li.find("span",attrs={"class":"money"})
		one.append(handler_price(price_tag.b.text.strip()))
		img_tag = li.find('img')
		one.append("http://www.momoshop.com.tw"+img_tag["src"])
		one.append(goods_name_tags.a["href"])
		one.append('')
		result.append(one)
	return result[0:count]

def handler_price(price):
	"""
	专用于处理形如xx.xx的价格， 过滤出price中的数字
	:param price 价格字符串
	"""
	if price.find(".") < 0:
		return get_number(price)
	else:
		head, tail = price.split(".")
		return "".join([get_number(head), ".", get_number(tail)])

def get_number(s):
	pattern = re.compile(u"[\d]")
	return filter(lambda x: re.match(pattern, x), s)



