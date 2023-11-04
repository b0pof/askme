from django.db import models
from django.contrib.auth.models import AbstractBaseUser


# User:
#  - email
#  - nickname
#  - password
#  - avatar
#  - date
#  - rating
class User(AbstractBaseUser):
    email = models.CharField(max_length=128)
    nickname = models.CharField(max_length=64)
    password = models.CharField(max_length=128)
    date = models.DateField()
    rating = models.FloatField()


# Question:
#  - title
#  - description
#  - author
#  - date
#  - tags
#  - rating
class Question(models.Model):
    id = models.PositiveBigIntegerField(primary_key=True)
    title = models.CharField(max_length=30)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    tags = models.TextField()
    rating = models.IntegerField()


# Answer:
#  - description
#  - author
#  - date 
#  - is_correct
#  - rating
#  - question
class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    is_correct = models.BooleanField()
    rating = models.FloatField()


# Tag:
#  - word
class Tag():
    word = models.CharField(max_length=32)

