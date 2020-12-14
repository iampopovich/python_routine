from django.shortcuts import render
from .models import Person, Company, Product
from .forms import UserForm, CustomForm, StylesForm, DatabaseForm
from .widgets import FormWithWidget
from django.template.response import TemplateResponse
from django.http import (
    HttpResponse,
    HttpResponseRedirect,
    HttpResponsePermanentRedirect,
    HttpResponseNotFound
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
        form = UserForm(data=req.POST)
        if form.is_valid():
            name = form.cleaned_data["field_name"]
            return HttpResponse("<h2>Hello, {0}</h2>".format(name))
        else:
            return HttpResponse("Invalid data")
    else:
        form = UserForm()
        return render(req, "userForm.html", {"form": form})


def widget_form(req):
    if req.method == "POST":
        return HttpResponse("<h2>You've sent a widget form</h2>")
    else:
        widgetform = FormWithWidget()
        return render(req, "formWidgets.html", {"form": widgetform})


def custom_form(req):
    if req.method == "POST":
        form = CustomForm(data=req.POST)
        if form.is_valid():
            name = form.cleaned_data["field_name"]
            return HttpResponse("<h2>Hello, {0}</h2>".format(name))
        else:
            return HttpResponse("Invalid data")
    else:
        form = CustomForm(
            field_order=["field_comment", "field_age",  "field_name"])
        return render(req, "customForm.html", {"form": form})


def styles_form(req):
    if req.method == "POST":
        form = StylesForm(data=req.POST)
        if form.is_valid():
            name = form.cleaned_data["field_name"]
            return HttpResponse("<h2>Hello, {0}</h2>".format(name))
        else:
            return HttpResponse("Invalid data")
    else:
        form = StylesForm()
        return render(req, "userFormStyles.html", {"form": form})


def add_person(req):
    if req.method == "POST":
        person = Person()
        person.name = req.POST.get("name")
        person.age = req.POST.get("age")
        person.save()
    return HttpResponseRedirect("/all_persons")


def all_persons(req):
    persons = Person.objects.all()
    return render(req, "all_persons.html", {"persons": persons})


def edit_person(req, id):
    try:
        person = Person.objects.get(id=id)
        if req.method == "POST":
            person.name = req.POST.get("name")
            person.age = req.POST.get("age")
            person.save()
            return HttpResponseRedirect("/all_persons")
        else:
            return render(req, "edit_person.html", {"person": person})
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def remove_person(req, id):
    try:
        person = Person.objects.get(id=id)
        person.delete()
        return HttpResponseRedirect("all_users")
    except Person.DoesNotExist:
        return HttpResponseNotFound("<h2>Person not found</h2>")


def show_companies(req):
    companies = Company.objects.all()
    return render(req, "all_companies.html", {"companies": companies})


def add_company(req):
    if req.method == "POST":
        company = Company()
        company.name = req.POST.get("name")
        company.save()
    return HttpResponseRedirect("/all_companies")


def show_company(req, id):
    company = Company.objects.get(id=id)
    products = Product.objects.all()
    return render(req, "company.html", {"company": company, "products": products})


def remove_company(req, id):
    try:
        company = Company.objects.get(id=id)
        company.delete()
        return HttpResponseRedirect("/all_companies")
    except Company.DoesNotExist:
        return HttpResponseNotFound("<h2>Company not found</h2>")
