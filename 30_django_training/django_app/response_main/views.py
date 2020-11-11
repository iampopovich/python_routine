from django.shortcuts import render
from django.http import HttpResponse


def index(req):
    return HttpResponse("<h2>Главная</h2>")


def about(req):
    return HttpResponse("<h2>Инфо</h2>")


def help(req):
    return HttpResponse("<h2>Помощь</h2>")


def contact(req):
    return HttpResponse("<h2>Контакты</h2>")


def regular_middleware(req):
    return HttpResponse("<h2>you got regexp processed path</h2>")
