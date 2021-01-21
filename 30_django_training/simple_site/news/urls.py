from django.urls import path, re_path, include
from django.views.generic import ListView, DetailView
from news.models import Articles
from . import views

urlpatterns = [
    re_path(r'^$', ListView.as_view(
        queryset=Articles.objects.all().order_by("-date")[:20],
        template_name='news/posts.html')),
    path(r'<int:pk>', DetailView.as_view(
        model=Articles,
        template_name='news/post.html')),
    re_path(r'^get_all_articles$', views.get_all_articles)
]
