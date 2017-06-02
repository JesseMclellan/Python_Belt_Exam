# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from .models import User, UserManager
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
        return redirect('/logged_in')
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
        return redirect('/logged_in')
        # return render(request, 'dojo_secrets_app/secrets.html')
    #if login is not valid return redirect('/')
    for error in login_validation:
        messages.info(request, error)
        print "something happened"
        return redirect('/')

def logged_in(request):
    return render(request, 'python_belt_apps/logged_in.html')

def logging_out(request):
    logout(request)
    messages.info(request, 'you are successfully logged out')
    # request.session.clear()
    return redirect('/')
