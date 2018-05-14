#! /usr/bin/env python3
# coding: utf-8
import xml.etree.ElementTree as et
from urllib.request import urlopen
import sys
import readline
import os
import time

CACHE_PATH = os.path.expanduser('~') + '/.yd'

# 命令行交互
url_query = 'http://fanyi.youdao.com/openapi.do?keyfrom=majunzhe&key=27448872&type=data&doctype=xml&version=1.1&q='

isword = True
def get_xml(word):
	global isword
	li = []
	for c in word:
		w = ''
		for i in c.encode('utf-8'):
			w += '%' + hex(i)[2:]
		li.append(w)
	word = ''.join(li)
	if '%20' in word:
		isword = False
	else:
		isword = True
	url = url_query + word
	data = urlopen(url).read().decode('utf-8')
	return data

# format string for outputing
word_fs = '\t英： {}\n\t基本释义:\n\t\t{}\n\t网络释义:\n\t\t{}'
p_fs = '\t基本释义:\n\t\t{}\n\t网络释义:\n\t\t{}'
def parse_xml(data):
	root = et.fromstring(data)
	if isword:
		phonetic = root.find('.//phonetic').text.replace('\n', '')
		# us_phone = root.find('.//us-phonetic').text.replace('\n', '')
		basic = root.find('basic')
		basic_ex = ''
		for ex in basic.findall('.//ex'):
			basic_ex += ex.text.replace('\n', '') + '\n\t\t'
		basic_ex = basic_ex.rstrip('\n\t\t')
	else:
		paragraph = root.find('.//paragraph').text.replace('\n', '')
	web = root.find('web')
	web_ex = ''
	if web is not None:
		for explain in web.findall('explain'):
			web_ex += explain.find('key').text.replace('\n', '') + ' '
			for ex in explain.findall('./value/ex'):
				web_ex += ex.text.replace('\n', '') + ','
			web_ex += '\n\t\t'
		web_ex = web_ex.rstrip('\n\t\t')
	if isword:
		res = word_fs.format(phonetic, basic_ex, web_ex) + '\n'
	else:
		res = p_fs.format(paragraph, web_ex) + '\n'
	return res


# 保存单词结果，可供日后查阅
def save_to_file(word, result):
	'''
		保存每个单词的查询历史，及查询结果，保存到文件还是数据库?
		每个单词建立一个文件作为索引
		统计查询次数最多的单词
	'''
	if not os.path.exists(CACHE_PATH):
		os.mkdir(CACHE_PATH)
	result_path = os.path.join(CACHE_PATH, word + '.result')
	cache_path = os.path.join(CACHE_PATH, word + '.history')
	# 保存结果
	with open(result_path, 'w') as fd:
		fd.write(result)
	# 保存查询时间
	with open(cache_path, 'a') as fd:
		fd.write('{} [{}]\n'.format(int(time.time()), time.strftime('%Y-%m-%d %H:%M:%S')))


def find_top_words(n, start_time):
	'''
		列出某个时间点之后最经常查询的单词
	'''
	pass



def go_ahead(word):
	data = get_xml(word)
	try:
		result = parse_xml(data)
		save_to_file(word, result) 
		print(result)
	except AttributeError as e:
	# raise e
		print('没有结果')

def main():
	if len(sys.argv) > 1:
		for word in sys.argv[1:]:
			go_ahead(word)
			print('-'*80)
	else:
		while True:
			word = input('>>> ')
			if '@' == word:
				break
			go_ahead(word)
if __name__ == '__main__':
	main()