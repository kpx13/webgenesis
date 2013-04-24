# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem
import pytils


class WorkTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        slug = tag.lower().replace(' ', '-')
        if i is not None:
            slug += '-%d' % i
        return slug

class WorkTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return WorkTag

class Work(models.Model):
    title = models.CharField(max_length=256, verbose_name=u'заголовок')
    href = models.CharField(max_length=256, blank=True, verbose_name=u'ссылка')
    desc = models.TextField(blank=True, verbose_name=u'описание')
    order = models.SmallIntegerField(blank=True, default=0, verbose_name=u'порядок')
    slug = models.SlugField(verbose_name=u'slug', unique=True, blank=True)
    tags = TaggableManager(through=WorkTaggedItem, blank=True)
    date = models.DateField(verbose_name=u'дата выполнения проекта', blank=True)
    
    class Meta:
        verbose_name = u'работа'
        verbose_name_plural = u'работы'
        ordering = ['-order']
        
    def __unicode__(self):
        return self.title
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.translify(self.title).lower().replace(' ', '-').replace('\'', '')
        super(Work, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return Work.objects.get(slug=slug)
        except:
            return None
        
    @staticmethod
    def get_recent(count=3):
        return list(Work.objects.all()[:count])
    
    @staticmethod
    def get_by_tag(tag=None):
        if not tag:
            return []
        else:
            return list(Work.objects.filter(tags__slug__in=[tag]))
        
class Image(models.Model):
    work = models.ForeignKey(Work, verbose_name=u'работа', related_name='image')
    image = models.ImageField(upload_to='uploads/items', max_length=256, blank=True, verbose_name=u'изображение')
    order = models.IntegerField(null=True, blank=True, default=100, verbose_name=u'порядок сортировки')

    @staticmethod
    def get(id_):
        try:
            return Image.objects.get(id=id_)
        except:
            return None
    
    class Meta:
        verbose_name = u'изображение'
        verbose_name_plural = u'изображения'
        ordering=['order']
        
    def __unicode__(self):
        return str(self.id) 
        