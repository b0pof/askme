from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from blog.models import Question, Answer
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
        description = "Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy? Hi. I'm wondering why that Los Pollos chicken is that tasty. I wanna cook it at home but have some doubts about the receipt. Is there a way to make it so crispy?"
        q.description = description
        q.author = User()
        q.author.username = random.choice(["Flynn", "Walter Hartwell White Jr.", "Walt Jr."]) 
        q.creation_date = "%02d.%02d.%04d" % (random.randint(1, 28), random.randint(1, 12), random.randint(2007, 2023))

        q.tags = list()
        for _ in range(2):
            q.tags.append(random.choice(POPULAR_TAGS))

        q.rating = round(random.randint(-20, 20))
        questions.append(q)

    return questions


def make_anwers(amount: int) -> [Answer]:
    answers = list()

    for i in range(amount):
        a = Answer()
        a.id = 576 + i
        description = "First, Gus gets deliveries every day, so the food is always fresh. Second, Gus is almost always on the premises so the workers are on the ball. three, Gus is actually a good boss. He hires ambitious people to manage, makes sure people work the shifts they want, and is generally helpful."
        a.description = description
        a.author = User()
        a.author.username = random.choice(["Sam", "Bob", "Thomas", "Joseph", "Michael", "Charles"]) 
        a.creation_date = "%02d.%02d.%04d" % (random.randint(1, 28), random.randint(1, 12), random.randint(2007, 2023))
        a.is_correct = random.randint(0, 1)
        a.rating = round(random.randint(-20, 20))

        answers.append(a)

    return answers


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
