from django.shortcuts import render
from django.views.generic import ListView, DetailView
from news.models import Articles
from django.core.serializers import serialize, deserialize
from django.http import HttpResponse



def get_all_articles(request):
    return ListView.as_view(
        queryset=Articles.objects.all().order_by("-date")[:20],
        template_name='news/posts.html')(request)

def get_serialized_data(request):
	    return HttpResponse(serialize("json", Articles.objects.all()))
