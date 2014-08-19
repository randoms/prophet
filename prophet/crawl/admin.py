from django.contrib import admin

# Register your models here.
from crawl import models

class DocumentAdmin(admin.ModelAdmin):
    pass

class CommentAdmin(admin.ModelAdmin):
    pass

admin.site.register(models.News)
admin.site.register(models.Keywords)
admin.site.register(models.Refers)