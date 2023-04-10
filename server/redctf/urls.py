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
from django.conf.urls.static import static
from django.urls import re_path
from django.urls import path, include
from redctf import views
from django.views.decorators.csrf import csrf_exempt
from graphene_django.views import GraphQLView
from graphene_file_upload.django import FileUploadGraphQLView


urlpatterns = [
    #django admin
    path('djangoadmin/', admin.site.urls),

    path("logs/", include("log_viewer.urls")),
    
    #ctf admin
    path('adminpanel/', views.admin_panel, name='admin_panel'),

    ################ dashboard #################
    path('adminpanel/dashboard/', views.dashboard, name='dashboard'),
    ############################################

    ################ categories ################
    path('adminpanel/category/', views.category_list, name='category_list'),
    path('adminpanel/category/new/', views.category_new, name='category_new'),
    path('adminpanel/category/<int:pk>/', views.category_detail, name='category_detail'),
    path('adminpanel/category/<int:pk>/edit/', views.category_edit, name='category_edit'),
    path('adminpanel/category/<int:pk>/delete/', views.category_delete, name='category_delete'),
    ############################################

    ################ challenges ################
    path('adminpanel/challenge/', views.challenge_list, name='challenge_list'),
    path('adminpanel/challenge/new/', views.challenge_new, name='challenge_new'),
    path('adminpanel/challenge/<int:pk>/', views.challenge_detail, name='challenge_detail'),
    path('adminpanel/challenge/<int:pk>/edit/', views.challenge_edit, name='challenge_edit'),
    path('adminpanel/challenge/<int:pk>/delete/', views.challenge_delete, name='challenge_delete'),
    ############################################

    ################ containers ################
    path('adminpanel/container/', views.container_list, name='container_list'),
    # path('adminpanel/container/new/', views.container_new, name='container_new'),
    path('adminpanel/container/<int:pk>/', views.container_detail, name='container_detail'),
    # path('adminpanel/container/<int:pk>/edit/', views.container_edit, name='container_edit'),
    path('adminpanel/container/<int:pk>/delete/', views.container_delete, name='container_delete'),
    path('adminpanel/container/delete/', views.container_delete_all, name='container_delete_all'),
    ############################################

    ################ ctfs ################
    path('adminpanel/ctf/', views.ctf_list, name='ctf_list'),
    path('adminpanel/ctf/new/', views.ctf_new, name='ctf_new'),
    path('adminpanel/ctf/<int:pk>/', views.ctf_detail, name='ctf_detail'),
    path('adminpanel/ctf/<int:pk>/edit/', views.ctf_edit, name='ctf_edit'),
    path('adminpanel/ctf/<int:pk>/delete/', views.ctf_delete, name='ctf_delete'),
    ############################################

    ################## teams ###################
    path('adminpanel/team/', views.team_list, name='team_list'),
    path('adminpanel/team/new/', views.team_new, name='team_new'),
    path('adminpanel/team/<int:pk>/', views.team_detail, name='team_detail'),
    path('adminpanel/team/<int:pk>/edit/', views.team_edit, name='team_edit'),
    path('adminpanel/team/<int:pk>/delete/', views.team_delete, name='team_delete'),
    ############################################

    ################## users ###################
    path('adminpanel/user/', views.user_list, name='user_list'),
    path('adminpanel/user/new/', views.user_new, name='user_new'),
    path('adminpanel/user/<int:pk>/', views.user_detail, name='user_detail'),
    path('adminpanel/user/<int:pk>/edit/', views.user_edit, name='user_edit'),
    path('adminpanel/user/<int:pk>/delete/', views.user_delete, name='user_delete'),
    ############################################

    #path('graphql/', csrf_exempt(GraphQLView.as_view(graphiql=True))),
    path('graphql/', csrf_exempt(FileUploadGraphQLView.as_view(graphiql=True))),
]

if settings.DEBUG:
    urlpatterns += [
        re_path(r'^static/(?P<path>.*)$', staticfiles.views.serve),
    ]
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    
urlpatterns += staticfiles_urlpatterns()
