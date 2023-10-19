from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from blog.models import Question
from django.contrib.auth.models import User
from random import uniform


"""
TO-DO:
1) HTML CSS:
 - ask
 - settings
 - question
 - search bar

2) functions:
 - tag searching
"""

def make_question(amount: int) -> [Question]:
    questions = list()

    for i in range(amount):
        q = Question()
        q.id = 347923 + i
        q.title = "How to cook chicken properly?"
        q.description = "Hi. I'm wondering why that Los Poilos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Poilos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? "
        q.author = User()
        q.author.first_name = "Flynn"
        q.creation_date = "08.10.2009"
        q.tags = [tag for tag in "Cooking, Chicken, Los Poilos, Gustavo Fring".split(",")]
        q.rating = round(uniform(1.5, 5.0), 1)

        questions.append(q)

    return questions


def new(request):
    template = loader.get_template('index.html')
    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]
    questions = make_question(50)
    
    title = "New Questions"
    subtitle = "Hot Questions"

    return HttpResponse(template.render({"questions": questions, "tags": tags, "title": title, "subtitle": subtitle, "members": members, "loggedIn": 1, "name": "Saul Goodman"}, request))


def hot(request):
    template = loader.get_template('index.html')
    tags = ["Perl", "IT", "MySQL", "Django", "Go", "Docker", "Linux", "nginx", "Rust", "Mail.ru", "Firefox"]
    members = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]
    questions = make_question(50)
    hot_questions = [question for question in questions if float(question.rating) > 4]
    title = "Hot Questions"

    return HttpResponse(template.render({"questions": hot_questions, "tags": tags, "title": title, "members": members, "loggedIn": 1, "name": "Saul Goodman"}, request))


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
