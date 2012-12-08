# -*- coding: utf-8 -*-

from django.contrib import messages
from django.core.context_processors import csrf
from django.http import HttpResponseRedirect, HttpResponseNotFound
from django.shortcuts import render_to_response
from django.template import RequestContext

from request.forms import RequestForm
from pages.models import Page

ADMINS = ['ann@webgenesis.ru']

def send_mail_to_admin(data):
    from django.core.mail import send_mail
    text= u'Имя: ' + data['name'] + u"\n" + u'email: ' + data['email'] + '\n' + u'Телефон: ' + data['phone'] + '\n' + u'Текст: ' + data['comment'] + '\n'
    send_mail('Новое сообщение с сайта', text , 'noreply@webgenesis.ru', ADMINS, fail_silently=False)

def get_common_context(request):
    c = {}
    c['request_url'] = request.path
    c.update(csrf(request))
    return c

def home_page(request):
    c = get_common_context(request)
    c['request_url'] = 'home'
    c['content'] = Page.get_page_by_slug('home')['content']
    return render_to_response('home.html', c, context_instance=RequestContext(request))

def order_page(request):
    c = get_common_context(request)
    if request.method == 'GET':
        c['request_form'] = RequestForm()
    else:
        form = RequestForm(request.POST)
        if form.is_valid():
	    send_mail_to_admin(form.cleaned_data)
            form.save()
            form = RequestForm()
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
	return render_to_response('404.html', c, context_instance=RequestContext(request))
def insert_test_data(request):
    import test_data
    test_data.go_pages()
    return HttpResponseRedirect('/')
