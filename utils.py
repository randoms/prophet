#encoding=utf-8

import time
from pyquery import PyQuery as pq

def timestr_to_stamp(timestr):
	return time.time()

def get_title(page):
	# 从h1开始找，一直找到h4
	title = ""
	for count in range(1,5):
		title = page('h'+str(count)).text()
		if len(title) != 0:
			# 可能会有多个标题，取最长的那个
			title = title.split(' ')
			target_title = ""
			for mtitle in title:
				if len(mtitle) > len(target_title):
					target_title = mtitle
			title = target_title
			break;
	if page('title').eq(0).text() != None:
	 	newtitle = page('title').eq(0).text()
	 	if len(newtitle) > len(title):
	 		title = newtitle #取较长的作为标题
	title = get_title_1(title,page) # 遍历特殊的取标题方法
	return title

'''
start custom get title
'''
def get_title_1(title,page):
	if len(title) != 0:
		return title # title already found
	return title


def get_time_str(page):
	span = page("span")
	time_str = ""
	for count in range(0,len(span)):
		if (span.eq(count).attr('class') != None and span.eq(count).attr('class').find('time') != -1 ) \
		 or ( span.eq(count).attr('id') != None and span.eq(count).attr('id').find('time') != -1):
			time_str = span.eq(count).text()
	time_str = get_time_str_solidot(time_str,page) # 遍历特殊取时间方法
	return time_str

'''
start custom get time
'''
def get_time_str_solidot(time_str,page):
	if len(time_str) != 0:
		return time_str
	time_str = page('div.talk_time').eq(0).text()
	if time_str == None:
		time_str = ""
	return time_str


def get_time(page):
	time_str = get_time_str(page)
	mtime = timestr_to_stamp(time_str)
	return mtime

'''
start custom get content
'''
def get_content(page):
	content = page('html').text()
	#content = get_content_solidot(content, page)
	#content = get_content_idc(content,page)
	return content

def get_content_solidot(content,page):
	if len(content) != 0:
		return content
	content = page(".p_mainnew").html()
	if content == None:
		content = "" # content not found
	return content

def get_content_idc(content,page):
	if len(content) != 0:
		return content
	content = page(".left-container").html()
	if content == None:
		content = ""
	return content

'''
start custom get refer
'''
def get_refer(page):
    links = pq(refers)("a")
    refer = []
	for count in range(0, len(links)):
        refer.append(links.eq(count).attr('href'))
	#refer = get_refer_solidot(refer,page)
	return refer

def get_refer_solidot(refer,page):
	if len(refer) != 0:
		return refer
	refers = get_content(page)
	if len(refers) == 0:
		return [] # cannot find refer
	#find links in content
	links = pq(refers)("a")
	referlist = []
	for count in range(0, len(links)):
		referlist.append(links.eq(count).attr('href'))
	return referlist