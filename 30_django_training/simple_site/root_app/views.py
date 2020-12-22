from django.shortcuts import render
from django.http import HttpResponse
from datetime import date, datetime


def index(request):
    # is_true = datetime.now().month == 12
    return render(request, 'root_app/main_page.html',{})#, {"is_true":is_true})


def contact(request):
    return render(request, 'root_app/contacts.html', {'content': [
        'my name', '+100 000 999']})


