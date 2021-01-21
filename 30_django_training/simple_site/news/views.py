from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import Articles


def get_all_articles(request):
    return ListView.as_view(
        queryset=Articles.objects.all().order_by("-date")[:20],
        template_name='news/posts.html')(request)
