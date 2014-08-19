from django.shortcuts import render
from django.http import HttpResponse
from models import News, Keywords, Refers
import json
from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def add_news(req):
    check = News.objects.filter(link=req.POST['link'])
    mnews = ""
    if check.count() != 0:
        # record already exist
        if check[0].time > int(req.POST['time']):
            return HttpResponse(json.dumps({'status':'OK'},indent=4),content_type='application/json')
        mnews = check[0]
    else:
        mnews = News()
    mnews.title = req.POST['title']
    mnews.content = req.POST['content']
    mnews.link = req.POST['link']
    mnews.time = int(req.POST['time'])
    mnews.save()
    keywords = json.loads(req.POST['keywords'])
    refers = json.loads(req.POST['refers'])
    for word in keywords:
        mkeywords = Keywords()
        mkeywords.news = mnews
        mkeywords.words = word
        mkeywords.save()
    for refer in refers:
        mrefer = Refers()
        mrefer.news = mnews
        mrefer.refer = refer
        mrefer.save()
    return HttpResponse(json.dumps({'status':'OK'}),content_type='application/json')
