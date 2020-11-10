from django.shortcuts import render
from django.http import HttpResponse


def index(request='nothing'):
    return HttpResponse("You asked me {}".format(request))

