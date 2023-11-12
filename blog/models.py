from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import QuerySet
from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.utils.translation import gettext_lazy as _
from typing import List


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="media/")
    rating = models.IntegerField(default=0)

    def __str__(self) -> str:
        return self.user.username


class TagManager(models.Manager):
    def get_popular(self) -> List[str]:
        tags = []

        tag_objects = super().get_queryset(). \
            values('word'). \
            annotate(count=models.Count('question')). \
            order_by('-count')[:13]
        
        for tag in tag_objects:
            tags.append(tag["word"])
        return tags


class Tag(models.Model):
    word = models.CharField(blank=False, max_length=32)

    def __str__(self) -> str:
        return self.word
    
    objects = TagManager()


class Reaction(models.Model):
    class ReactionTypes(models.TextChoices):
        LIKE = "L", _("Like")
        DISLIKE = "D", _("Dislike")

    profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name="likes")
    content_type = models.ForeignKey(ContentType, on_delete=models.PROTECT)
    object_id = models.PositiveBigIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')
    reaction_type = models.CharField(max_length=1, choices=ReactionTypes.choices, default=ReactionTypes.LIKE)


class QuestionManager(models.Manager):
    def get_new(self) -> QuerySet:
        return super().get_queryset().order_by('creation_date').reverse()

    def get_hot(self) -> QuerySet:
        return super().get_queryset() \
            .annotate(r_count=(
                models.Count(
                    'reactions',
                    filter=models.Q(reactions__reaction_type="L")
                ) - 
                models.Count(
                    'reactions',
                    filter=models.Q(reactions__reaction_type="D")
                ))
            ).order_by('-r_count')

    def get_by_tag(self, tag) -> QuerySet:
        return super().get_queryset().filter(tags__word=tag)


class Question(models.Model):
    title = models.CharField(blank=False, max_length=100)
    description = models.TextField()
    author = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="question_author")
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    tags = models.ManyToManyField(Tag)
    reactions = GenericRelation(Reaction)

    objects = QuestionManager()

    def likes_count(self) -> int:
        return self.reactions.filter(reaction_type="L").count()

    def dislikes_count(self) -> int:
        return self.reactions.filter(reaction_type="D").count()

    def rating(self) -> int:
        return self.likes_count() - self.dislikes_count()
    
    def get_url(self) -> str:
        return f"/question/{self.id}"


class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, id) -> QuerySet:
        return super().get_queryset() \
            .filter(question_id=id) \
            .annotate(r_count=(
                models.Count(
                    'reactions',
                    filter=models.Q(reactions__reaction_type="L")
                ) -
                models.Count(
                    'reactions',
                    filter=models.Q(reactions__reaction_type="D")
                ))
            ).order_by('-r_count')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    description = models.TextField(blank=False)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    is_correct = models.BooleanField(default=False)
    reactions = GenericRelation(Reaction)

    objects = AnswerManager()

    def likes_count(self) -> int:
        return self.reactions.filter(reaction_type="L").count()

    def dislikes_count(self) -> int:
        return self.reactions.filter(reaction_type="D").count()

    def rating(self) -> int:
        return self.likes_count() - self.dislikes_count()

