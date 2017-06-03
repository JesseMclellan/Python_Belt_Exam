# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, UserManager, Quote, QuoteManager
from django.contrib import messages
from django.contrib.auth import logout
# Create your views here.
def index(request):
    return render(request, 'python_belt_apps/index.html')

def register(request):
    postData = {
        "first_name" : request.POST['first_name'],
        "last_name" : request.POST['last_name'],
        "email" : request.POST['email'],
        "password" : request.POST['password'],
        "conpass" : request.POST['conpass']
    }

    new_user = User.objects.register(postData)

    if len(new_user) == 0:
        request.session['id'] = User.objects.filter(email=postData['email'])[0].id
        request.session['name'] = postData['first_name']
        return redirect('/quo')
    else:
        for error in new_user:
            messages.info(request, error)
    return redirect('/')

def login(request):
    postData = {
        "email" : request.POST['email'],
        "password" : request.POST['password'],
    }

    login_validation = User.objects.login(postData)
    #if login is valid return redirect('dojo_secrets_app/secrets.html')t
    if len(login_validation) == 0:
        request.session['id'] = User.objects.get(email=postData['email']).id
        request.session['name'] = User.objects.get(email=postData['email']).first_name
        return redirect('/quo')
        # return render(request, 'dojo_secrets_app/secrets.html')
    #if login is not valid return redirect('/')
    for error in login_validation:
        messages.info(request, error)
        print "something happened"
        return redirect('/')

def quo(request):
    q1 = Quote.objects.all().order_by("-created_at")
    context = {
        "quotes" : q1,
        "currentuser" : User.objects.get(id=request.session['id'])
    }
    return render(request, 'python_belt_apps/quotes.html', context)

def post_quote(request):
    postData = {
        'post' : request.POST['author'] + ": "+ request.POST['quote'],
        "user_id" : request.session['id'],
    }
    post_submit = Quote.objects.post_submit(postData)
    for error in post_submit:
        messages.error(request, error)

    return redirect('/quo')

def favorite(request, id):
    result = Quote.objects.quotes_favorited(id, request.session['id'])
    return redirect('/quo')

def remove(request, id):
    return redirect('/quo')

def users(request, id):
    q1 = Quote.objects.all().order_by("-created_at")
    context = {
        "quotes" : q1,
        "currentuser" : User.objects.get(id=request.session['id'])
    }
    print "hi"
    print context['quotes']

    return render(request, 'python_belt_apps/users.html', context)

def logging_out(request):
    logout(request)
    messages.info(request, 'you are successfully logged out')
    return redirect('/')
