# -*- coding: utf-8 -*-

from django.conf import settings
from django.contrib import messages
from django.core.context_processors import csrf
from django.core.mail import EmailMessage
from django.http import HttpResponseRedirect, Http404
from django.shortcuts import render_to_response
from django.template import RequestContext
import pytils

from request.forms import RequestForm
from pages.models import Page
from portfolio.models import Work
from blog.models import Article
from slideshow.models import Slider

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c['works'] = Work.get_recent(4)
    c['articles'] = Article.get_recent(4)
    c.update(csrf(request))
    return c

def home_page(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['slideshow'] = Slider.get_slideshow()
    c['page'] = Page.get_by_slug('home')
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def portfolio_page(request, curr_work=None):
    c = get_common_context(request)
    if curr_work:
        c['curr_work'] = Work.get_by_slug(curr_work)
        return render_to_response('portfolio_work.html', c, context_instance=RequestContext(request))
    else:
        c['works'] = Work.objects.all()
        return render_to_response('portfolio.html', c, context_instance=RequestContext(request))

def articles_page(request, curr_work=None):
    c = get_common_context(request)
    if curr_work:
        c['curr_article'] = Article.get_by_slug(curr_work)
        return render_to_response('article.html', c, context_instance=RequestContext(request))
    else:
        c['articles'] = Article.objects.all()
        return render_to_response('articles.html', c, context_instance=RequestContext(request))

def order_page(request):
    c = get_common_context(request)
    if request.method == 'GET':
        c['request_form'] = RequestForm()
    else:
        form = RequestForm(request.POST)
        if form.is_valid():
            form.save()
            data = form.cleaned_data
            message= u'Имя: ' + data['name'] + u"\n" + u'email: ' + data['email'] + '\n' + u'Телефон: ' + data['phone'] + '\n' + u'Текст: ' + data['comment'] + '\n'
        
            email = EmailMessage(u'Новое сообщение с сайта', message, settings.EMAIL_HOST_USER, settings.REQUEST_SEND_TO)
            file = request.FILES.get('brief')
            if file: email.attach_file(handle_file(file))
            email.send()

            messages.success(request, u'Ваш запрос отправлен.')
            return HttpResponseRedirect('/')
        else:
            c['request_form'] = form
            messages.error(request, u'При обработке формы произошла ошибка.')
    c['page'] = Page.get_by_slug('order')
    return render_to_response('request.html', c, context_instance=RequestContext(request))

def other_page(request, page_name):
    c = get_common_context(request)
    try:
        c['page'] = Page.get_by_slug(page_name)
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    except:
        raise Http404

def contacts_page(request):
    c = get_common_context(request)
    return render_to_response('contacts.html', c, context_instance=RequestContext(request))

def umi_page(request):
    c = get_common_context(request)
    return render_to_response('umi.html', c, context_instance=RequestContext(request))
    
def handle_file(f):
    filename = settings.ROOT_FOR_ATTACES + pytils.translit.translify(f.name)
    destination = open(filename, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filename
