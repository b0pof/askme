from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from util.pagination.pagination import paginate
from util.mock.mock import *


def new(request):
    template = loader.get_template('index.html')
    questions = make_question(54)
    
    title = "New Questions"
    subtitle = "Hot Questions"

    return HttpResponse(
        template.render(
            {
                "questions": paginate(request, questions),
                "tags": POPULAR_TAGS,
                "title": title,
                "subtitle": subtitle,
                "members": MEMBERS,
                "loggedIn": 1,
                "name": "Saul Goodman"
            },
            request
        )
    )


def hot(request):
    template = loader.get_template('index.html')
    questions = make_question(50)
    hot_questions = [question for question in questions if float(question.rating) > 4]
    title = "Hot Questions"

    return HttpResponse(
        template.render(
            {
                "questions": paginate(request, hot_questions), 
                "tags": POPULAR_TAGS, 
                "title": title,
                "members": MEMBERS, 
                "loggedIn": 1,
                "name": "Saul Goodman"
            },
            request
        )
    )


def tag(request, tag):
    template = loader.get_template('index.html')
    questions = make_question(50)
    matched_questions = [question for question in questions if tag in question.tags]
    title = f'Tag: {tag}'

    return HttpResponse(
        template.render(
            {
                "questions": paginate(request, matched_questions),
                "tags": POPULAR_TAGS,
                "title": title,
                "members": MEMBERS,
                "loggedIn": 1,
                "name": "Saul Goodman"
            },
            request
        )
    )


def question(request, id):
    template = loader.get_template('question.html')
    question = make_question(1)[0]
    answers = make_anwers(31)

    return HttpResponse(
        template.render(
            {
                "question": question,
                "answers": answers,
                "title": f"Question {id}",
                "tags": POPULAR_TAGS,
                "members": MEMBERS,
                "name": "Saul Goodman",
                "loggedIn": 1
            },
            request
        )
    )


def login(request):
    template = loader.get_template('login.html')

    return HttpResponse(
        template.render(
            {
                "tags": POPULAR_TAGS,
                "members": MEMBERS,
                "loggedIn": 0
            },
            request
        )
    )


def signup(request):
    template = loader.get_template('signup.html')

    return HttpResponse(
        template.render(
            {
                "tags": POPULAR_TAGS,
                "members": MEMBERS,
                "loggedIn": 0
            },
            request
        )
    )


def ask(request):
    template = loader.get_template('ask.html')
    title = "New Question"

    return HttpResponse(
        template.render(
            {
                "title": title,
                "tags": POPULAR_TAGS,
                "members": MEMBERS,
                "name": "Saul Goodman",
                "loggedIn": 1
            },
            request
        )
    )


def settings(request):
    template = loader.get_template('settings.html')
    return HttpResponse(
        template.render(
            {
                "tags": POPULAR_TAGS,
                "username": "sAllGoodMan228",
                "members": MEMBERS,
                "name": "Saul Goodman",
                "loggedIn": 1
            },
            request
        )
    )
