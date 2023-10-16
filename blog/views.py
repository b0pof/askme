from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader


def new(request):
    template = loader.get_template('index.html')
    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]
    questions = [f"Question {i}" for i in range(1, 100)]

    return HttpResponse(template.render({"questions": questions, "tags": tags, "title": "New Questions", "members": members, "loggedIn": 1, "name": "Saul Goodman"}, request))


def hot(request):
    return render(request, 'index.html')


def tag(request):
    return render(request, 'index.html')


def question(request, id):
    template = loader.get_template('question.html')
    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]

    return HttpResponse(template.render({"title": f"Question {id}", "tags": tags, "members": members, "name": "Saul Goodman", "loggedIn": 1}, request))


def login(request):
    template = loader.get_template('login.html')

    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]

    return HttpResponse(template.render({"tags": tags, "members": members, "loggedIn": 0}, request))


def signup(request):
    template = loader.get_template('signup.html')

    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]

    return HttpResponse(template.render({"tags": tags, "members": members, "loggedIn": 0}, request))


def ask(request):
    template = loader.get_template('ask.html')
    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]

    return HttpResponse(template.render({"title": f"Question {id}", "tags": tags, "members": members, "name": "Saul Goodman", "loggedIn": 1}, request))


def settings(request):
    template = loader.get_template('settings.html')

    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]

    return HttpResponse(template.render({"tags": tags, "members": members, "name": "Saul Goodman", "loggedIn": 1}, request))
