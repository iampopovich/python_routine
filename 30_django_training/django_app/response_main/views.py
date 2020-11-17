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


def gadgets(req):
    return HttpResponse("<h2>here will be gadget list</h2>")


def products(req, product_id=20):
    out = "<h2>Product № {0}</h2>".format(product_id)
    return HttpResponse(out)


def users(req, user_id, user_name):
    out = "<h2>User</h2><h3>id: {0}  name: {1}</h3>".format(user_id, user_name)
    return HttpResponse(out)
