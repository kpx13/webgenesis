# -*- coding: utf-8 -*-
from django.contrib import admin
import models

class SliderAdmin(admin.ModelAdmin):
    list_display = ('title', 'show', 'sort_parameter')
    ordering = ('sort_parameter', )
    list_filter = ('show', )
    
admin.site.register(models.Slider, SliderAdmin)