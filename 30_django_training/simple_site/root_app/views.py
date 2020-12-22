from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return render(request, 'root_app/main_page.html', {})


def contact(request):
    return render(request, 'root_app/contacts.html', {'content':[
    	'my name', '+100 000 999']})
