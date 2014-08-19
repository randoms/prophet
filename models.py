#encoding=utf-8

'''
初始化数据库，建立对应的表
'''
import os
from storm.locals import *

mfiles = os.listdir(os.getcwd())
database = create_database("sqlite:m.db")
store = Store(database)

class News_m(object):
	__storm_table__ = "news"
	id = Int(primary=True)
	title = Unicode()
	time = Int() # 用时间戳来保存时间

	def save(self):
		store.add(self)
		store.commit()

class Keywords_m(object):
	__storm_table__ = "keywords"
	id = Int(primary=True)
	news_id = Int() # 目标新闻
	value = Unicode() #关键字内容

	def save(self):
		store.add(self)
		store.commit()

class UnparsePage_m(object):
	__storm_table__ = "unparse_page"
	id = Int(primary=True)
	url = Unicode()

	@staticmethod
	def print_all():
		for page in store.find(UnparsePage_m):
			print page.url

	def save(self):
		store.add(self)
		store.commit()

class News_source_m(object):
	__storm_table__ = "news_source"
	id = Int(primary=True)
	url = Unicode()

	@staticmethod
	def print_all():
		for page in store.find(News_source_m):
			print page.url

	def save(self):
		store.add(self)
		store.commit()

def init_db():
	if 'm.db' not in mfiles:
		# create db and tables
		store.execute("CREATE TABLE news "
   			"(id INTEGER PRIMARY KEY, title VARCHAR, time INTEGER)")
		store.execute("CREATE TABLE keywords "
			"(id INTEGER PRIMARY KEY, news_id INTEGER, value VARCHAR)")
		store.execute("CREATE TABLE unparse_page "
			"(id INTEGER PRIMARY KEY, url VARCHAR)")
		store.execute("CREATE TABLE news_source "
			"(id INTEGER PRIMARY KEY, url VARCHAR)")
