from django.shortcuts import render
from django.http import HttpResponse


def new(request):
    return render(request, 'base.html')


def hot(request):
    return render(request, 'base.html')


def tag(request):
    return render(request, 'index.html')


def question(request):
    return render(request, 'question.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    return render(request, 'ask.html')


def settings(request):
    return render(request, 'settings.html')
