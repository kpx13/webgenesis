# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class ArticleAdmin(admin.ModelAdmin):
    list_display = ('slug', 'date', 'title')
    search_fields = ('title', 'content')
    ordering = ('date', )

admin.site.register(models.Article, ArticleAdmin)