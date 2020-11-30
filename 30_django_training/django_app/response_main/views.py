from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect
)


def index(req):
    header = "Personal Data"
    langs = ["English", "German", "Spanish"]
    user = {"name": "Tom", "age": 23}
    addr = ("Абрикосовая", 23, 45)
    data = {"header": header, "langs": langs, "user": user, "address": addr}
    return TemplateResponse(req, "index.html", data)


def help(req):
    return HttpResponse("<h2>Помощь</h2>")


def details(request):
    return HttpResponsePermanentRedirect("/")


def regular_middleware(req):
    return HttpResponse("<h2>you got regexp processed path</h2>")


def gadgets(req):
    return HttpResponse("<h2>here will be gadget list</h2>")


def products(req, product_id=20):
    category = req.GET.get("cat", "")
    out = "<h2>Product № {0} of category {1}</h2>".format(product_id, category)
    return HttpResponse(out)


def users(req):
    user_id = req.GET.get("user_id", 20)
    user_name = req.GET.get("user_name", "Robert")
    out = "<h2>User</h2><h3>id: {0}  name: {1}</h3>".format(user_id, user_name)
    return HttpResponse(out)
