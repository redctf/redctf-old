"""redctf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.conf import settings
from django.contrib import staticfiles
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import re_path
from django.urls import path
from redctf import views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView

urlpatterns = [
    #django admin
    path('admin/', admin.site.urls),
    
    #ctf admin
    path('adminpanel/', views.admin_panel, name='admin_panel'),

    ################ challenges ################
    path('challenge/', views.challenge_list, name='challenge_list'),
    path('challenge/new/', views.challenge_new, name='challenge_new'),
    path('challenge/<int:pk>/', views.challenge_detail, name='challenge_detail'),
    path('challenge/<int:pk>/edit/', views.challenge_edit, name='challenge_edit'),
    path('challenge/<int:pk>/delete/', views.challenge_delete, name='challenge_delete'),
    ############################################

    ################ containers ################
    path('container/', views.container_list, name='container_list'),
    # path('container/new/', views.container_new, name='container_new'),
    # path('container/<int:pk>/', views.container_detail, name='container_detail'),
    # path('container/<int:pk>/edit/', views.container_edit, name='container_edit'),
    # path('container/<int:pk>/delete/', views.container_delete, name='container_delete'),
    ############################################

    ################## teams ###################
    path('team/', views.team_list, name='team_list'),
    path('team/new/', views.team_new, name='team_new'),
    path('team/<int:pk>/', views.team_detail, name='team_detail'),
    path('team/<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('team/<int:pk>/delete/', views.team_delete, name='team_delete'),
    ############################################

    ################## users ###################
    path('user/', views.user_list, name='user_list'),
    path('user/new/', views.user_new, name='user_new'),
    path('user/<int:pk>/', views.user_detail, name='user_detail'),
    path('user/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('user/<int:pk>/delete/', views.user_delete, name='user_delete'),
    ############################################

    #path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', staticfiles.views.serve),
    ]

urlpatterns += staticfiles_urlpatterns()