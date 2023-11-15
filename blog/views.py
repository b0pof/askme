from django.shortcuts import render
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.template import loader
from util.pagination.pagination import paginate
from util.mock.mock import *
from blog.models import Question, Answer, Profile, Tag


def add_context(context: dict) -> None:
    # context["tags"] = ["lol", "ask", "try"]
    # context["members"] = ["user1", "user2", "user3"]
    context["tags"] = Tag.objects.get_popular()
    context["members"] = Profile.objects.get_top_users()


def new(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('index.html')
    questions = Question.objects.get_new()

    try:
        pages = paginate(request, questions)
    except Exception as ex:
        return HttpResponseNotFound("<h1>Page not found</h1>")
    
    context = {
        "questions": pages,
        "title": "New Questions",
        "subtitle": "Hot Questions",
        "loggedIn": 1,
        "name": "Saul Goodman"
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def hot(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('index.html')
    questions = Question.objects.get_hot()

    try:
        pages = paginate(request, questions)
    except Exception:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    context = {
        "questions": pages, 
        "title": "Hot Questions",
        "loggedIn": 1,
        "name": "Saul Goodman"
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def tag(request: HttpRequest, tag: str) -> HttpResponse:
    template = loader.get_template('index.html')

    questions = Question.objects.get_by_tag(tag)

    title = f'Tag: {tag}'
    if questions.count() == 0:
        title = f"No questions with tag '{tag}'"

    try:
        pages = paginate(request, questions)
    except Exception:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    context = {
        "questions": pages,
        "title": title,
        "loggedIn": 1,
        "name": "Saul Goodman"
    }
    add_context(context)
    
    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def question(request: HttpRequest, id: int) -> HttpResponse:
    template = loader.get_template('answers.html')

    question = Question.objects.get(pk=id)
    answers = Answer.objects.get_answers_by_question_id(id)

    try:
        pages = paginate(request, answers)
    except Exception as ex:
        return HttpResponseNotFound("<h1>Page not found</h1>")

    context = {
        "question": question,
        "answers": pages,
        "title": f"Question {id}",
        "tags": Tag.objects.get_popular(),
        "members": MEMBERS,
        "name": "Saul Goodman",
        "loggedIn": 1
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def login(request: HttpRequest) -> HttpResponse:
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


def signup(request: HttpRequest) -> HttpResponse:
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


def ask(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('ask.html')

    context = {
        "title": "New Question",
        "name": "Saul Goodman",
        "loggedIn": 1
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def settings(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('settings.html')

    context = {
        "username": "sAllGoodMan228",
        "name": "Saul Goodman",
        "loggedIn": 1
    }
    add_context(context)
    
    return HttpResponse(
        template.render(
            context,
            request
        )
    )
