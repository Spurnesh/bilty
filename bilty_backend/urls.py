"""bilty_backend URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from django.urls import path, include
from core import views
from django.contrib.auth.views import LogoutView

urlpatterns = [
    path('bilty/', include('bilty.urls')),
    path('admin/', admin.site.urls),
    path('login/', views.LoginView.as_view()),
    path('', views.Dashboard.as_view()),
    path('logout/', LogoutView.as_view(),name='logout'),
    path('add-bilty/', views.BiltyCreateView.as_view()),
    path('view-bilty/', views.BiltyListView.as_view()),
    path('add-user/', views.UserCreateView.as_view()),
    path('view-user/', views.UserListView.as_view()),
]
