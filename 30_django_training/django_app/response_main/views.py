from django.shortcuts import render
from .forms import UserForm, CustomForm
from .widgets import FormWithWidget
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


def details(req):
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


def conditions(req):
    data = {"num": int(req.GET.get("num", 0))}
    print(data)
    return render(req, "format_conditions.html", context=data)


def iterators(req):
    langs = ["English", "German", "French", "Spanish", "Chinese"]
    return render(req, "format_iterators.html", context={"langs": langs})


def user_form(req):
    if req.method == "POST":
        name = req.POST.get("name")
        age = req.POST.get("age")
        return HttpResponse("<h2>Hello, {0}, heh {1}</h2>".format(name, age))
    else:
        userform = UserForm()
        return render(req, "userForm.html", {"form": userform})


def widget_form(req):
    if req.method == "POST":
        return HttpResponse("<h2>You've sent a widget form</h2>")
    else:
        widgetform = FormWithWidget()
        return render(req, "formWidgets.html", {"form": widgetform})


def custom_form(req):
    if req.method == "POST":
        return HttpResponse("<h2>You've sent a custom form</h2>")
    else:
        customform = CustomForm(
            field_order=["field_comment", "field_age",  "field_name"])
        return render(req, "customForm.html", {"form": customform})
