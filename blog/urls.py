from django.urls import path
from . import views

urlpatterns = [
    path('ask', views.ask, name='blog-ask'),
    path('base', views.base, name='blog-base'),
    path('index', views.index, name='blog-index'),
    path('login', views.login, name='blog-login'),
    path('question', views.question, name='blog-question'),
    path('signup', views.signup, name='blog-signup'),
]
