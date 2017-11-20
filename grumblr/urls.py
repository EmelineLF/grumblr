from django.conf.urls import url, include
from django.contrib import admin
from django.contrib.auth import views as auth_views

from . import views
from webapps import views as views_apps


urlpatterns = [
	url(r'^$', views_apps.login_redirect, name='login_redirect'),
    url(r'^login/$', views.login, {'template_name': 'grumblr/login.html'}, name='login'),
    url(r'^logout$', auth_views.logout,{'template_name': 'grumblr/logout.html'}, name='logout'),
    url(r'^post/', views.new_post, name='new_post'),
    url(r'^signup/$', views.register, name='register'),
    url(r'^feed/$', views.feed, name='feed'),
    url(r'^profil/(?P<username>[a-zA-Z0-9]+)$', views.profil, name='profil'),
    url(r'^profil/edit/$', views.edit, name='edit'),
    url(r'^reset-password/$', auth_views.password_reset, {'template_name':'grumblr/reset.html'}, name='password_reset'),
    url(r'^reset-password/done$', auth_views.password_reset_done,{'template_name':'grumblr/reset_done.html'}, name='password_reset_done'),
    url(r'^reset-password/confirm/(?P<uidb64>[0-9A-Za-z]+)-(?P<token>.+)/$', auth_views.password_reset_confirm,{'template_name':'grumblr/reset_confirm.html'},  name='password_reset_confirm'),
    url(r'^reset-password/complete/$', auth_views.password_reset_complete,{'template_name':'grumblr/reset_complete.html'}, name='password_reset_complete'),
    url(r'^activate/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>[0-9A-Za-z]{1,13}-[0-9A-Za-z]{1,20})/$', views.activate, name='activate'),
    url(r'^feed/get_posts/$', views.get_posts, name='get_posts'),
    url(r'^comment/(?P<postid>[0-9A-Za-z_\-]+)', views.comment, name='new_comment'),
    url(r'^feed/get_comments/(?P<postid>[0-9A-Za-z_\-]+)', views.get_comments, name='get_comments'),

]

