# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver




class Post(models.Model):
    user = models.ForeignKey(User)
    content = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_posts(user):
        return Post.objects.filter(user=user).order_by("date").reverse()
    def __unicode__(self):
        return self.content
    def __str__(self):
        return self.__unicode__()

class Comment(models.Model):
    user = models.ForeignKey(User)
    text = models.TextField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, related_name='comments')

    @staticmethod
    def __unicode__(self):
        return self.text
    def __str__(self):
        return self.__unicode__()

class UserProfil(models.Model):
    user = models.OneToOneField(User)
    age = models.IntegerField(null=True, blank=True, default=0)
    bio = models.TextField(max_length=420,blank=True, default='')
    picture = models.ImageField(upload_to='pictures/', blank=True, default='/pictures/nopicture.png')
    followees = models.ManyToManyField(User, related_name='followees', symmetrical=False)

    def __unicode__(self):
        return self.user.username
    def __str__(self):
        return self.__unicode__()


