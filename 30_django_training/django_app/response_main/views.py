from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return HttpResponse("<h2>Главная</h2>")


def about(req):
    return HttpResponse("<h2>Инфо</h2>")


def help(req):
    return HttpResponse("<h2>Помощь</h2>")
