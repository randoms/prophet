#encoding=utf-8
from pyquery import PyQuery as pq

import urllib
import jieba
from threadpool import *
from models import init_db,UnparsePage_m,store,News_source_m
from utils import get_title, get_time, get_content, get_refer
import time
import 

def win_print(str):
	#print str.encode("GBK","ignore");
	print str

'''
新闻对象
@param
	link 新闻的链接地址

'''
class news:

	def __init__(self,link):
		self.link = link
		self.title = ""
		self.time = 0
		self.content = ""
		self.keywords = ""
		self.refer = []
		self.status = False # 是否解析成功
        
        # 检查是否在已解析的连接里面
        
		# 检查是否在无法解析的名单内
		if link.find('http://') == -1:
			return # invalid link
		base_url = 'http://' + link.split('/')[2]
		# unparse_check = store.find(UnparsePage_m, UnparsePage_m.url == base_url.decode('utf-8'))
		# if unparse_check.count() != 0:
			# print "can not parse this link"
			# return
		self.pq = ""
		try:
			self.pq = pq(url=link).make_links_absolute() #可能会解析失败
		except Exception as err: 
			print "failed to open this link " + link
		if self.pq == "":
			return
		# get title
		self.title = get_title(self.pq)
		self.time = time.time()
		self.content = get_content(self.pq)
		self.refer = get_refer(self.pq)
		if len(self.title) == 0 or \
		len(self.content) == 0 or len(self.refer) == 0:
			# 无法成功解析
			print "can not parse " + link
			# 把网址添加异常网站数据库
			mpage = UnparsePage_m()
			mpage.url = base_url.decode('utf-8')
			mpage.save()
			self.keywords = ''
			return
		else:
			# get keywords
			self.keywords = jieba.cut_for_search(self.title)
		self.status = True

	def get_info(self):
		win_print("title: "+self.title)
		win_print("time: "+str(self.time))
		win_print("keywords: "+", ".join(self.keywords))
		win_print("content: "+self.content)
		win_print("refer: ");
		print self.refer

	'''
	添加到新闻源之中
	'''
	def add_to_source(self):
		# check if already exsit
		source = News_source_m()
		source.url =('http://' + self.link.split('/')[2]).decode('utf-8')
		if store.find(News_source_m, News_source_m.url == source.url).count() == 0:
			print "saving"
			source.save()


'''
爬行一个新闻，并且把该页面引用的新闻加入到任务列表,这里要递归调用
'''

pool = ThreadPool(20)

def crawl_news(link):
	mnews = news(link)
	if mnews.status:
		mnews.add_to_source()
		if len(mnews.refer) != 0:
			# 开新线程
			requests = makeRequests(crawl_news, mnews.refer)
			[pool.putRequest(req) for req in requests]

def init_record():
    
    
    
init_db()
init_record()
# mnews.get_info()
# crawl_news("http://www.solidot.org/story?sid=40747")
# pool.wait()

print "my source"
News_source_m.print_all()

print "error page"
UnparsePage_m.print_all()