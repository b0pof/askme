from django.shortcuts import render
from django.http import HttpResponse, HttpResponseNotFound
from django.template import loader
from django.db.models import Max, Count
from util.pagination.pagination import paginate
from util.mock.mock import *
from blog.models import Question, Answer, Profile, Tag
import random


def new(request) -> HttpResponse:
    template = loader.get_template('index.html')

    questions = Question.objects.get_new()
    tags = Tag.objects.get_popular()

    try:
        pages = paginate(request, questions)
    except Exception as ex:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    return HttpResponse(
        template.render(
            {
                "questions": pages,
                "tags": tags,
                "title": "New Questions",
                "subtitle": "Hot Questions",
                "members": MEMBERS,
                "loggedIn": 1,
                "name": "Saul Goodman"
            },
            request
        )
    )


def hot(request) -> HttpResponse:
    template = loader.get_template('index.html')

    questions = Question.objects.get_hot()

    try:
        pages = paginate(request, questions)
    except Exception:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    return HttpResponse(
        template.render(
            {
                "questions": pages, 
                "tags": Tag.objects.get_popular(), 
                "title": "Hot Questions",
                "members": MEMBERS, 
                "loggedIn": 1,
                "name": "Saul Goodman"
            },
            request
        )
    )


def tag(request, tag) -> HttpResponse:
    template = loader.get_template('index.html')

    questions = Question.objects.get_by_tag(tag)

    title = f'Tag: {tag}'
    if questions.count() == 0:
        title = f"No questions with tag '{tag}'"

    try:
        pages = paginate(request, questions)
    except Exception:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    
    return HttpResponse(
        template.render(
            {
                "questions": pages,
                "tags": Tag.objects.get_popular(),
                "title": title,
                "members": MEMBERS,
                "loggedIn": 1,
                "name": "Saul Goodman"
            },
            request
        )
    )


def question(request, id) -> HttpResponse:
    template = loader.get_template('question.html')

    question = Question.objects.get(pk=id)
    answers = Answer.objects.get_answers_by_question_id(id)

    return HttpResponse(
        template.render(
            {
                "question": question,
                "answers": answers,
                "title": f"Question {id}",
                "tags": Tag.objects.get_popular(),
                "members": MEMBERS,
                "name": "Saul Goodman",
                "loggedIn": 1
            },
            request
        )
    )


def login(request) -> HttpResponse:
    template = loader.get_template('login.html')

    return HttpResponse(
        template.render(
            {
                "tags": Tag.objects.get_popular(),
                "members": MEMBERS,
                "loggedIn": 0
            },
            request
        )
    )


def signup(request) -> HttpResponse:
    template = loader.get_template('signup.html')

    return HttpResponse(
        template.render(
            {
                "tags": Tag.objects.get_popular(),
                "members": MEMBERS,
                "loggedIn": 0
            },
            request
        )
    )


def ask(request) -> HttpResponse:
    template = loader.get_template('ask.html')

    return HttpResponse(
        template.render(
            {
                "title": "New Question",
                "tags": Tag.objects.get_popular(),
                "members": MEMBERS,
                "name": "Saul Goodman",
                "loggedIn": 1
            },
            request
        )
    )


def settings(request) -> HttpResponse:
    template = loader.get_template('settings.html')
    
    return HttpResponse(
        template.render(
            {
                "tags": Tag.objects.get_popular(),
                "username": "sAllGoodMan228",
                "members": MEMBERS,
                "name": "Saul Goodman",
                "loggedIn": 1
            },
            request
        )
    )
