# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.conf import settings
from django.contrib.auth.views import login as contrib_login
from django.shortcuts import render, redirect
from django.contrib.auth.models import User
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm, PasswordChangeForm
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from .tokens import account_activation_token
from django.contrib.auth.models import User
from django.core.mail import EmailMessage
from django.core import serializers
from django.http import HttpResponse
from forms import *
from models import *

# Create your views here.
def login(request, **kwargs):
    if request.user.is_authenticated():
        return redirect(settings.LOGIN_REDIRECT_URL)
    else:
        return contrib_login(request, **kwargs)

def register(request):    
    context = {}

    if request.method == 'GET':
        context['form'] = RegistrationForm()
        return render(request, 'grumblr/registration.html', context)

    form = RegistrationForm(request.POST)
    context['form'] = form

    if not form.is_valid():
        context['error']="Your username and password didn't match. Please try again."
        return render(request, 'grumblr/registration.html', context)

    # context['error']
    new_user = User.objects.create_user(username=form.cleaned_data['username'], 
                                        password=form.cleaned_data['password1'],
                                        first_name=form.cleaned_data['first_name'],
                                        last_name=form.cleaned_data['last_name'],
                                        email=form.cleaned_data['email'])
    
    new_user.is_active = False
    new_user.save()
    new_user = authenticate(username=form.cleaned_data['username'], \
                            password=form.cleaned_data['password1'])


    profile=UserProfil(user=new_user)
    profile.save()
    current_site = get_current_site(request)
    mail_subject = 'Activate your blog account.'
    message = render_to_string('acc_active_email.html', {
                   'user': new_user,
                    'domain': current_site.domain,
                    'uid':urlsafe_base64_encode(force_bytes(new_user.pk)),
                    'token':account_activation_token.make_token(new_user),
            })
    to_email = form.cleaned_data.get('email')
    email = EmailMessage(
                     mail_subject, message, to=[to_email]
            )
    email.send()

    
    return render (request, 'grumblr/activate.html', context)

def activate(request, uidb64, token):
    context={}
    try:
        uid = force_text(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        context['user']=user
        return render(request, 'grumblr/activate_complete.html', context)
    else : 
        return render(request, 'grumblr/activate_complete.html', context)

@login_required
def feed(request): 
    context={}   
    if request.method=='GET' or ('all' in request.POST):        
        form = CreatePostForm()
        context['form'] = form
        context['user']= request.user
        context['posts'] = Post.objects.order_by("date").reverse()
        return render(request, 'grumblr/feed.html', context)
    elif 'Post' in request.POST :
        new_post = Post(content=request.POST.get('content'),user=request.user)       
        new_post.save()
        return HttpResponse("")
    elif 'follower' in request.POST : 
        form = CreatePostForm()
        context['posts']=[]
        followees = request.user.userprofil.followees.all()
        context['posts'] = Post.objects.filter(user__in=followees).order_by('date').reverse()
        context['form'] = form
        context['user']= request.user
        return render(request, 'grumblr/feed.html', context)
    elif 'comment' in request.POST : 
        new_comment = Comment(post=Post.objects.get(id=postid),text=request.POST.get('text'),user=request.user)       
        new_comment.save()
        return HttpResponse("")

def get_posts(request):
    posts = Post.objects.order_by('date').reverse().distinct()
    return render(request, 'posts.json', {"posts":posts} , content_type="grumblr/json")

def get_comments(request,postid):
    comments = Comment.objects.get(post=Post.objects.get(id=postid)).distinct()
    return render(request , 'comments.json', {'comments':comments} , content_type="grumblr/json")

@login_required
def profil(request, username):
    context={}

    if request.user==User.objects.get(username=username):
        user=request.user
        context['profile']=user.userprofil
        context['username']= user
        context['posts'] = Post.objects.filter(user=user).order_by("date").reverse()
        return render(request,'grumblr/myprofil.html',context)
    else :
        user=User.objects.get(username=username)
        context['profile']=user.userprofil
        context['following']=(user in request.user.userprofil.followees.all())
        context['username']= user
        context['posts'] = Post.objects.filter(user=user).order_by("date").reverse()
        if request.method=='GET':        
            return render(request, 'grumblr/profil.html', context)
        else :
             return follow(request,context)

@login_required
def follow(request,context):
    print('hello')
    followees=request.user.userprofil.followees
    print(followees.all())
    if context['following']:
        followees.remove(context['username'])        
    else :
        request.user.userprofil.followees.add(context['username'])
    request.user.userprofil.save()
    print(request.user.userprofil.followees.all())
    return redirect(reverse('profil',args=[context['username']]))

@login_required
def new_post(request):
    if request.method=='GET':
        return HttpResponse("")
    else :
        new_post = Post(content=request.POST.get('content'),user=request.user)       
        new_post.save()
        return HttpResponse("")

@login_required
def comment(request, postid):
    if request.method=='GET':
        return redirect('feed')
    else :
        new_comment = Comment(post=Post.objects.get(id=postid),text=request.POST.get('text'),user=request.user)       
        new_comment.save()
        print(Post.objects.get(id=postid).comments.all)
        return redirect('feed')

@login_required
def edit(request):
    context={}
    if request.method=='GET':
        profile_form = UpdateProfil(initial={'user':request.user,'first_name':request.user.first_name,'last_name':request.user.last_name},instance=request.user.userprofil)
        context['form']=profile_form
        return render(request, 'grumblr/editprofil.html', context)
    else : 
        profile_form = UpdateProfil(request.POST or None,request.FILES, instance=request.user.userprofil)
        if profile_form.is_valid():
            user=request.user
            request.user.first_name=request.POST.get('first_name')
            request.user.last_name=request.POST.get('last_name')
            print(request.POST.get('password'))
            if request.POST.get('password')!='':
                request.user.set_password(request.POST.get('password'))
            profile_form.save()
            request.user.save()   
            login(request, request.user, backend='django.contrib.auth.backends.ModelBackend')
            print(request.user.username)         
            return redirect(reverse('profil',args=[request.user.username]))
        else : 
            context['form']=profile_form
            return render(request, 'grumblr/editprofil.html', context)

