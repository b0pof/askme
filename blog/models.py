from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Question(models.Model):
    title = models.CharField(max_length=30)
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    tags = models.TextField()
    rating = models.FloatField()


class Answer(models.Model):
    description = models.TextField()
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    creation_date = models.DateField()
    isCorrect = models.BooleanField()
    rating = models.FloatField()
