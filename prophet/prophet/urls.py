from django.conf.urls import patterns, include, url

from django.contrib import admin
import crawl.views as crawl

admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'prophet.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^news/add$',crawl.add_news)
)
