from django.shortcuts import render, redirect
from django.http import HttpRequest, HttpResponse, HttpResponseNotFound
from django.template import loader
from util.pagination.pagination import paginate
from util.mock.mock import *
from blog.models import Question, Answer, Profile, Tag, User
from django.core.cache import cache
from django.contrib import auth
from django.urls import reverse
from blog.forms import LoginForm, SignupForm, SettingsForm, AskForm
from django.contrib.auth.decorators import login_required


def add_context(context: dict) -> None:
    top_tags = cache.get('top_tags')
    if top_tags == None:
        top_tags = Tag.objects.get_popular()
    
    top_members = cache.get('top_users')
    if top_members == None:
        top_members = Profile.objects.get_top_users()
    
    context["tags"] = top_tags
    context["members"] = top_members


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
        # "name": "Saul Goodman"
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
        # "name": "Saul Goodman"
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
        # "name": "Saul Goodman"
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
        # "name": "Saul Goodman",
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


def login(request: HttpRequest) -> HttpResponse:
    if request.user.is_authenticated:
        return redirect("/")
    
    template = loader.get_template('login.html')

    # print("GET", request.GET)
    # print("POST", request.POST)

    login_form = LoginForm()

    if request.method == "POST":
        login_form = LoginForm(request.POST)

        if login_form.is_valid():
            user = auth.authenticate(request, **login_form.cleaned_data)

            if user:
                auth.login(request, user)
                return redirect(request.POST.get("continue", "/"))
            else:
                login_form.add_error(field="password", error="Wrong password")

    return HttpResponse(
        template.render(
            {
                'login_form': login_form,
            },
            request=request
        )
    )


def logout(request: HttpRequest) -> HttpResponse:
    auth.logout(request)
    return redirect(reverse('login-page'))


def signup(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('signup.html')

    if request.user.is_authenticated:
        return redirect("/")

    signup_form = SignupForm()

    if request.method == "POST":
        print("POST:", request.POST)
        signup_form = SignupForm(request.POST)
        print("AFTER POST:", signup_form.data)

        if signup_form.is_valid():
            try:
                signup_form.save()
            except Exception as ex:
                print(f"Ex: {ex}")
                # signup_form.add_error(field="username", error="Such username already exists")

            user = auth.authenticate(request, **signup_form.cleaned_data)
            if user:
                auth.login(request, user)
                return redirect(request.POST.get("continue", "/"))
            else:
                signup_form.add_error("username", "Account wasn't created")

    return HttpResponse(
        template.render(
            {'signup_form': signup_form,},
            request=request
        )
    )


@login_required(login_url="/login", redirect_field_name="continue")
def ask(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('ask.html')
    # askForm = AskForm()

    if request.user.is_authenticated:
        if request.method == "POST":
            askForm = AskForm(request.POST)

            if askForm.is_valid():
                try:
                    new_question = Question.objects.create(
                        author=Profile.objects.filter(user=request.user)[0],
                        title=askForm.cleaned_data['title'],
                        description=askForm.cleaned_data['description'],
                    )
                    for tag in askForm.cleaned_data.get('tags', '').split(","):
                        existing_tag = Tag.objects.get(word=tag.strip(" "))
                        if existing_tag:
                            new_question.tags.add(existing_tag)
                        else:
                            new_tag = Tag.objects.create(word=tag.strip(" "))
                            new_question.tags.add(new_tag)
                except Exception as ex:
                    print(f"Question creation error: {ex}")

    context = {
        'ask_form': AskForm(),
    }
    add_context(context)

    return HttpResponse(
        template.render(
            context,
            request
        )
    )


@login_required(login_url="/login", redirect_field_name="continue")
def settings(request: HttpRequest) -> HttpResponse:
    template = loader.get_template('settings.html')
    settingsForm = SettingsForm()

    if request.user.is_authenticated:
        settingsForm = SettingsForm(
            data={
                'email': request.user.email,
                'username': request.user.username,
                # 'avatar': request.user.profile.avatar,
            } 
        )

        if request.method == "POST":
            settingsForm = SettingsForm(request.POST)

            if settingsForm.is_valid():
                try:
                    User.objects.filter(id=request.user.id).update(
                        email=settingsForm.cleaned_data.get("email", ""),
                        username=settingsForm.cleaned_data.get("username", ""),
                    )
                    Profile.objects.filter(id=request.user.id).update(
                        avatar=settingsForm.cleaned_data.get("avatar", ""),
                    )
                except Exception as ex:
                    print(f"Update error: {ex}")

    context = {'settings_form': settingsForm}
    add_context(context)
    
    return HttpResponse(
        template.render(
            context,
            request
        )
    )
