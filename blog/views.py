from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def new(request):
    template = loader.get_template('index.html')
    questions = [f"Question {i}" for i in range(1, 100)]

    return HttpResponse(template.render({"questions": questions, "title": "New Questions", "loggedIn": 1, "name": "Saul Goodman"}, request))


def hot(request):
    return render(request, 'index.html')


def tag(request):
    return render(request, 'index.html')


def question(request):
    return render(request, 'question.html')


def login(request):
    return render(request, 'login.html')


def signup(request):
    return render(request, 'signup.html')


def ask(request):
    template = loader.get_template('ask.html')
    return HttpResponse(template.render({"loggedIn": True, "name": "Saul Goodman"}, request))


def settings(request):
    return render(request, 'settings.html')
