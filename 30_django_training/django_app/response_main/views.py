from django.shortcuts import render
from django.template.response import TemplateResponse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect
)


def index(req):
    data = {"header": "Hello Django", "message": "Welcome to Python"}
    return render(req, "index.html", context=data)


def about(req):
    return HttpResponse("About")


def help(req):
    return HttpResponse("<h2>Помощь</h2>")


def contact(req):
    return HttpResponseRedirect("/about")


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
