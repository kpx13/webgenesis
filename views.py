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
from portfolio.models import Category, Work

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c.update(csrf(request))
    return c

def home_page(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['works'] = Work.objects.all()
    c['content'] = Page.get_page_by_slug('home')['content']
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def portfolio_page(request, curr_cat=None, curr_work=None):
    c = get_common_context(request)
    c['categories'] = Category.get_not_empty()
    c['curr_cat'] = Category.get_by_slug(curr_cat)
    if c['curr_cat'] is None:
        c['curr_cat'] = c['categories'][0]
    c['curr_work'] = Work.get_by_slug(curr_work)
    if c['curr_work'] is None:
        c['curr_work'] = Work.get_first_in_category(c['curr_cat'])
    return render_to_response('portfolio.html', c, context_instance=RequestContext(request))

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
        
            email = EmailMessage(u'Новое сообщение с сайта', message, settings.EMAIL_HOST_USER, settings.REQUEST_TO)
            file = request.FILES.get('brief')
            if file: email.attach_file(handle_file(file))
            email.send()

            messages.success(request, u'Ваш запрос отправлен.')
            return HttpResponseRedirect('/')
        else:
            c['request_form'] = form
            messages.error(request, u'При обработке формы произошла ошибка.')
    c.update(Page.get_page_by_slug('order'))
    return render_to_response('request.html', c, context_instance=RequestContext(request))

def other_page(request, page_name):
    c = get_common_context(request)
    try:
        c.update(Page.get_page_by_slug(page_name))
        return render_to_response('page.html', c, context_instance=RequestContext(request))
    except:
        raise Http404
    
def handle_file(f):
    filename = settings.ROOT_FOR_ATTACES + pytils.translit.translify(f.name)
    destination = open(filename, 'wb+')
    for chunk in f.chunks():
        destination.write(chunk)
    destination.close()
    return filename
