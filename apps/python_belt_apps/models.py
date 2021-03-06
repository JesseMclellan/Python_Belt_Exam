# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt
import re
NAME_REGEX =re.compile('^[A-z]+$')
EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')


class UserManager(models.Manager):
    def register(self, postData):
        errors = []
        if User.objects.filter(email=postData['email']):
            errors.append('Email is already registered')

        if postData['first_name'] == "" or postData['last_name'] == "" or postData['email'] == "" or postData['password'] == "" or postData['conpass'] == "":
            errors.append("Please fill out all fields")

        if len(postData['first_name']) <2 or len(postData['last_name']) <2:
            errors.append("Both first and last names must be at least 2 characters")

        if len(postData['email']) <1:
            errors.append('Email cannot be empty')
        elif not EMAIL_REGEX.match(postData['email']):
            errors.append('Invalid email format')

        if len(postData['password']) < 8:
            errors.append('Password must be at least 8 characters')
        elif postData["password"] != postData['conpass']:
            errors.append('Password do not match')


        if len(errors) == 0:
            salt = bcrypt.gensalt()
            password = postData['password'].encode()
            hashed_pw = bcrypt.hashpw(password, salt)

            User.objects.create(first_name=postData['first_name'], last_name=postData['last_name'],email=postData['email'],password=hashed_pw)
        return errors
    def login(self,postData):
        errors=[]
        # check if the email in the database or not
        if postData['email'] == "" or postData['password'] == "":
            errors.append("Please fill out all fields")

        if User.objects.filter(email=postData['email']):
            # encode the password to a specific format since the above email is registered
            login_pw = postData['password'].encode()
            # encode the registered user's password from database to a specific format
            db_pw = User.objects.get(email=postData['email']).password.encode()
            # compare the password with the password in database
            if not bcrypt.checkpw(login_pw, db_pw):
                errors.append('Incorrect password')

        else:
            errors.append("Email has not been registered")
        return errors

    # insert code

class User(models.Model):
    first_name = models.CharField(max_length=38)
    last_name = models.CharField(max_length=38)
    email = models.CharField(max_length=38)
    password = models.CharField(max_length=38)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __unicode__(self):
        return "id: " + str(self.id) +", first_name: " + self.first_name+ ", last_name: " + self.last_name+ ", email: " + self.email + ", password: " + str(self.password)




class QuoteManager(models.Manager):
    def post_submit(self, postData):
        errors = []
        if len(postData['post']) < 3:
            errors.append("No quote typed to post :(...)")
        if len(errors) == 0:
            Quote.objects.create(content=postData['post'], user_id=postData['user_id'])
        return errors

    def quotes_favorited(self, quoteid, userid):
        user = User.objects.get(id=userid)
        print user
        favo = Quote.objects.favorited()
        print favo
        fav = Quote.favorited.add(user)
        # fav = Quote.favorited(quotes_liked=Quote, user=user)

        print fav
        # try:
        #     qoute = self.get(id=quoteid)
        # except:
        #     return (False, "This secret is not found in our database!")
        # user = User.objects.get(id=userid)
        # if secret.user == user:
        #     return (False, "You can't like your own secret!")
        # secret.likers.add(user)
        # return (True, "You liked this secret!")
        return fav

        # Quote.favorited.get(qoute_id=quote_id).remove

class Quote(models.Model):
    content = models.CharField(max_length=38)
    user = models.ForeignKey(User, related_name="Quote")
    favorited = models.ManyToManyField(User, related_name="quotes_liked")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __unicode__(self):
        return "id: " + str(self.id) +", content: " + self.content+ ", user: " + str(self.user)
