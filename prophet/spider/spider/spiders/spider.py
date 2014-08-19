#encoding=utf-8

import scrapy
from scrapy.contrib.spiders import CrawlSpider, Rule
from scrapy.contrib.linkextractors import LinkExtractor
from pyquery import PyQuery as pq
import time
from scrapy.selector import Selector
import jieba
import requests
import json
import threading
import time

class DmozSpider(CrawlSpider):
    name = "baidu"
    allowed_domains = ["baidu.com"]
    start_urls = [
        "http://www.baidu.com"
    ]
    
    IGNORED_EXTENSIONS = [
        # images
        'mng', 'pct', 'bmp', 'gif', 'jpg', 'jpeg', 'png', 'pst', 'psp', 'tif',
        'tiff', 'ai', 'drw', 'dxf', 'eps', 'ps', 'svg',

        # audio
        'mp3', 'wma', 'ogg', 'wav', 'ra', 'aac', 'mid', 'au', 'aiff',

        # video
        '3gp', 'asf', 'asx', 'avi', 'mov', 'mp4', 'mpg', 'qt', 'rm', 'swf', 'wmv',
        'm4a',

        # office suites
        'xls', 'xlsx', 'ppt', 'pptx', 'doc', 'docx', 'odt', 'ods', 'odg', 'odp',

        # other
        'css', 'pdf', 'exe', 'bin', 'rss', 'zip', 'rar',
    ]
    rules = (Rule(LinkExtractor(deny_extensions=IGNORED_EXTENSIONS), callback='parse_item'),)

    def parse_item(self, response):
        page = pq(response.body).make_links_absolute(base_url=response.url)
        
        item = {}
        item['title'] = get_title(page)
        item['content'] = page('body').remove('script').remove('style').remove('template').text()
        keywords = ' '.join(jieba.cut(item['title']))
        item['keywords'] = keywords.split(' ')
        item['time'] = int(time.time()*1000)
        links = page("a")
        refer = []
        for count in range(0, len(links)):
            if links.eq(count).attr('href').find('http://') != -1:
                refer.append(links.eq(count).attr('href'))
        item['refers'] = refer
        item['link'] = response.url
        # save item to database
        send_server(item)
        return None
    
    
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
    return title

taskqueue = []
task_thread = None
con = threading.Condition()

def send_server(mnews):
    params = {'title':mnews['title'],
              'content':mnews['content'],
              'link':mnews['link'],
              'time':mnews['time'],
              'keywords':json.dumps(mnews['keywords'],indent=4),
              'refers':json.dumps(mnews['refers'],indent=4)}
    global con,taskqueue,task_thread
    con.acquire()
    taskqueue.append(params)
    con.release()
    if task_thread == None:
        # start work thread
        task_thread = MyThread()
        task_thread.start()

class MyThread(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
    def run(self):
        global taskqueue,con
        while True:
            params = None
            con.acquire()
            if len(taskqueue) != 0:
                print str(len(taskqueue)) + " task pending"
                params = taskqueue[0]
                taskqueue.remove(taskqueue[0])
            con.release()
            if params != None:
                r = requests.post("http://127.0.0.1/news/add", data=params)
            time.sleep(0.01)