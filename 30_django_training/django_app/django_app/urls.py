"""django_app URL Configuration

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
# from django.contrib import admin
from django.urls import path, re_path
from response_main import views
from django.views.generic import TemplateView

urlpatterns = [
    path('', views.index),
    path('about/', TemplateView.as_view(template_name="about.html",
                                        extra_context={"header": "О сайте"})),
    path('extended/', TemplateView.as_view(template_name="extended.html")),
    path('contact/', TemplateView.as_view(template_name="contact.html")),
    path('details/', views.details),
    path('dates/', TemplateView.as_view(template_name="format_dates.html")),
    path('context/', TemplateView.as_view(template_name="format_context.html")),
    path('cnds/', views.conditions),
    path('iters/', views.iterators),
    path('forms/', views.user_form),
]
