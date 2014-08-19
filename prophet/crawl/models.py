#encoding=utf-8
from django.db import models

# Create your models here.
class News(models.Model):
    '''
    the crawl result
    '''
    title = models.TextField()
    content = models.TextField()
    time = models.IntegerField()
    link = models.TextField(unique=True)
    
class Keywords(models.Model):
    news = models.ForeignKey(News,related_name='keywords')
    words = models.TextField()
    
class Refers(models.Model):
    news = models.ForeignKey(News, related_name='refer_news')
    refer = models.TextField()