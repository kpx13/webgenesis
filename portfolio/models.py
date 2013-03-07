# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField

import pytils

class Category(models.Model):
    slug = models.SlugField(verbose_name=u'slug', unique=True, blank=True)
    title = models.CharField(max_length=256, verbose_name=u'заголовок')
    desc = models.TextField(blank=True, verbose_name=u'описание')
    
    class Meta:
        verbose_name = u'категория'
        verbose_name_plural = u'категории'
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug=pytils.translit.translify(self.title).lower().replace(' ', '-').replace('\'', '')
        super(Category, self).save(*args, **kwargs)
    
    @staticmethod
    def get_not_empty():
        return [x for x in Category.objects.all() if Work.get_first_in_category(x)]
    
    @staticmethod
    def get_by_slug(slug):
        try:
            if slug:
                return Category.objects.get(slug=slug)
            else:
                return None 
        except:
            return None


class Work(models.Model):
    category = models.ForeignKey(Category, verbose_name=u'категория')
    slug = models.SlugField(verbose_name=u'slug', unique=True, blank=True)
    title = models.CharField(max_length=256, verbose_name=u'заголовок')
    href = models.CharField(max_length=256, blank=True, verbose_name=u'ссылка')
    image = models.FileField(upload_to= 'portfolio', blank=True, max_length=256, verbose_name=u'картинка')
    desc = models.TextField(blank=True, verbose_name=u'описание')
    order = models.SmallIntegerField(blank=True, default=0, verbose_name=u'порядок')
    
    class Meta:
        verbose_name = u'работа'
        verbose_name_plural = u'работы'
        ordering = ['-order']
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        self.slug=pytils.translit.translify(self.title).lower().replace(' ', '-').replace('\'', '')
        super(Work, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            if slug:
                return Work.objects.get(slug=slug)
            else:
                return None 
        except:
            return None
        
    @staticmethod
    def get_first_in_category(category):
        try:
            return Work.objects.filter(category=category)[0]
        except:
            return None
    
    @property
    def next(self):
        works = Work.objects.filter(category=self.category)
        l = len(works)
        for i in range(0, l):
            if works[i] == self:
                if i + 1 < l:
                    return works[i + 1]
                else:
                    return None
                
    @property
    def prev(self):
        works = Work.objects.filter(category=self.category)
        l = len(works)
        for i in range(0, l):
            if works[i] == self:
                if i - 1 >=0 :
                    return works[i - 1]
                else:
                    return None