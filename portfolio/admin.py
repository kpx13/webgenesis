# -*- coding: utf-8 -*-
from django.contrib import admin
from models import Work, Image

class ImageInline(admin.StackedInline): 
    model = Image
    extra = 3
    
class WorkAdmin(admin.ModelAdmin):
    inlines = [ ImageInline, ]
    list_display = ('slug', 'title', 'href', 'order', 'date')


admin.site.register(Work, WorkAdmin)