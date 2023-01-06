"""tdmh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.urls import path, include, re_path
from index import views
from login import views2


urlpatterns = [
    path('login/', views2.login,name='login'),
    path('login/find/',views.email),
    path('code/',views.find_code,name='code'),
    path('re_password/',views.re_password,name='re_password'),
    path('login_out/',views2.login_out),
    path('register/', views2.register),
    path('box/', include('index.urls')),
    path('admin/', views.admin, name='admin'),
    path('', views.hi),
    re_path(r'(?P<name>.*)/info/', views2.info,name='info'),
    path('change_head/', views.change_head),
    path('fold_create/',views.fold),
    path('fold/<int:id>/',views.fold2,name='fold2'),
    re_path(r'ad_fold/(?P<name>.*)/(?P<box>.*)/',views.fold3)
]
