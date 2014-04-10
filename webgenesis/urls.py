# -*- coding: utf-8 -*-

from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
from filebrowser.sites import site
admin.autodiscover()

import settings
import views

urlpatterns = patterns('',
    (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
	
    url(r'^admin_tools/', include('admin_tools.urls')),
    url(r'^admin/filebrowser/', include(site.urls)),
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^admin/jsi18n/', 'django.views.i18n.javascript_catalog'),
    url(r'^ckeditor/', include('ckeditor.urls')),

    url(r'^$' , views.home_page),
    url(r'^order/$' , views.order_page),
    url(r'^umi/$' , views.umi_page),
    url(r'^services/$' , views.services_page),
    url(r'^about/$' , views.about_page),
    url(r'^contacts/$' , views.contacts_page),
    url(r'^portfolio/$' , views.portfolio_page),
    url(r'^articles/$' , views.articles_page),
    url(r'^portfolio/(?P<curr_work>[\w-]+)/$' , views.portfolio_page),
    url(r'^articles/(?P<curr_work>[\w-]+)/$' , views.articles_page),
    url(r'^(?P<page_name>[\w-]+)/$' , views.other_page),
    
)
