from django.shortcuts import render
from django.http import HttpResponse


def base(request):
    return render(request, 'blog/base.html')


def ask(request):
    return render(request, 'blog/ask.html')


def index(request):
    return render(request, 'blog/index.html')


def login(request):
    return render(request, 'blog/login.html')


def question(request):
    return render(request, 'blog/question.html')


def signup(request):
    return render(request, 'blog/signup.html')
