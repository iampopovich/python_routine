from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse('<h2>Nice to meet you on styled_app</h2>')
