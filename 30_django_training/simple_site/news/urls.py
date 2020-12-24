from django.urls import re_path, include
from django.views.generic import ListView, DetailView
from news.models import Articles

urlpatterns = [
    re_path(r'^$', ListView.as_view(
        queryset=Articles.objects.all().order_by("-date")[:20],
        template_name='news/posts.html')),

]
