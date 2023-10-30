from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from blog.models import Question
from django.contrib.auth.models import User
from util.pagination.pagination import paginate
import random


# Mocks
POPULAR_TAGS = [tag for tag in "Cooking,Chicken,Pollos,Fring,Albuquerque,Laundry,Blue,Tight".split(",")]
MEMBERS = ["Gene Takovic", "Kimberly Wexler", "Lalo Salamanka", "Gustavo Fring", "Mike Hermantraut", "Victor"]


# Mock generator
def make_question(amount: int) -> [Question]:
    questions = list()

    for i in range(amount):
        q = Question()
        q.id = 347923 + i
        q.title = "How to cook chicken properly?"
        description = "Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy?"
        q.description = " ".join(description.split()[:50]) + "..."
        q.author = User()
        q.author.username = "Flynn"
        q.creation_date = "08.10.2009"

        q.tags = list()
        for _ in range(2):
            q.tags.append(random.choice(POPULAR_TAGS))

        q.rating = round(random.randint(-20, 20))
        questions.append(q)

    return questions


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

    return HttpResponse(
        template.render(
            {
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
