# -*- coding: utf-8 -*-
from django.db import models
from ckeditor.fields import RichTextField
import pytils
from taggit.managers import TaggableManager
from taggit.models import Tag, TaggedItem


class ArticleTag(Tag):
    class Meta:
        proxy = True

    def slugify(self, tag, i=None):
        slug = tag.lower().replace(' ', '-')
        if i is not None:
            slug += '-%d' % i
        return slug

class ArticleTaggedItem(TaggedItem):
    class Meta:
        proxy = True

    @classmethod
    def tag_model(cls):
        return ArticleTag

class Article(models.Model):
    name = models.CharField(max_length=128, verbose_name=u'название')
    date = models.DateField(verbose_name=u'дата')
    text = RichTextField(verbose_name=u'текст')
    desc = models.CharField(max_length=512, verbose_name=u'сокращенный текст')
    tags = TaggableManager(through=ArticleTaggedItem)
    slug = models.SlugField(verbose_name=u'slug', unique=True, blank=True, help_text=u'Заполнять не нужно')
   
    class Meta:
        verbose_name = u'статья'
        verbose_name_plural = u'статьи'
        ordering = ['-date']
    
    def __unicode__(self):
        return self.name
    
    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug=pytils.translit.slugify(self.name)
        super(Article, self).save(*args, **kwargs)
        
    @staticmethod
    def get_by_slug(slug):
        try:
            return Article.objects.get(slug=slug)
        except:
            return None
    
    @staticmethod
    def get_recent(count=4):
        return list(Article.objects.all()[:count])
    
    @staticmethod
    def get_by_tag(tag=None):
        if not tag:
            return []
        else:
            return list(Article.objects.filter(tags__slug__in=[tag]))