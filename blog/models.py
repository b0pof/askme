from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.db.models import QuerySet, Q
from django.utils.translation import gettext_lazy as _
from typing import List


class ProfileManager(models.Manager):
    def get_top_users(self) -> List[str]:
        users = []
        
        top_users = Question.objects.annotate(count=            # during the last week
            models.Count(
                'questionreaction',
                filter=models.Q(questionreaction__reaction_type="L")
            ) - 
            models.Count(
                'questionreaction',
                filter=models.Q(questionreaction__reaction_type="D")
            )
        ).order_by("-count").values("author__user__username")[:5]

        for value in top_users:
            users.append(value["author__user__username"])
                
        return users


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.PROTECT, null=True)
    avatar = models.ImageField(null=True, blank=True, upload_to="media/")
    rating = models.IntegerField(default=0)

    objects = ProfileManager()

    def __str__(self) -> str:
        return self.user.username


class TagManager(models.Manager):
    def get_popular(self) -> List[str]:         # During the last 3 months
        tags = []

        tag_objects = self. \
            values('word'). \
            annotate(count=models.Count('question')). \
            order_by('-count')[:10]
        
        for tag in tag_objects:
            tags.append(tag["word"])
        return tags


class Tag(models.Model):
    word = models.CharField(blank=False, max_length=32, unique=True)

    def __str__(self) -> str:
        return self.word
    
    objects = TagManager()


class QuestionManager(models.Manager):
    def get_new(self) -> QuerySet:
        return self.order_by('-creation_date')

    def get_hot(self) -> QuerySet:
        return self.annotate(r_count=(
            models.Count(
                'questionreaction',
                filter=models.Q(questionreaction__reaction_type="L")
            ) - 
            models.Count(
                'questionreaction',
                filter=models.Q(questionreaction__reaction_type="D")
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

    objects = QuestionManager()

    def likes_count(self) -> int:
        return QuestionReaction.objects.filter(reaction_type="L", question=self.id).count()

    def dislikes_count(self) -> int:
        return QuestionReaction.objects.filter(reaction_type="D", question=self.id).count()

    def rating(self) -> int:
        return self.likes_count() - self.dislikes_count()
    
    def get_url(self) -> str:
        return f"/question/{self.id}"


class AnswerManager(models.Manager):
    def get_answers_by_question_id(self, id) -> QuerySet:
        return self.filter(question_id=id) \
            .annotate(r_count=(
                models.Count(
                    'answerreaction',
                    filter=models.Q(answerreaction__reaction_type="L")
                ) -
                models.Count(
                    'answerreaction',
                    filter=models.Q(answerreaction__reaction_type="D")
                ))
            ).order_by('-r_count')


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    description = models.TextField(blank=False)
    author = models.ForeignKey(Profile, on_delete=models.PROTECT)
    creation_date = models.DateTimeField(default=timezone.now, editable=False)
    is_correct = models.BooleanField(default=False)

    objects = AnswerManager()

    def likes_count(self) -> int:
        return AnswerReaction.objects.filter(reaction_type="L", answer=self.id).count()

    def dislikes_count(self) -> int:
        return AnswerReaction.objects.filter(reaction_type="D", answer=self.id).count()

    def rating(self) -> int:
        return self.likes_count() - self.dislikes_count()


class QuestionReaction(models.Model):
    class ReactionTypes(models.TextChoices):
        LIKE = "L", _("Like")
        DISLIKE = "D", _("Dislike")

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="question_reactions")
    question = models.ForeignKey(Question, on_delete=models.PROTECT)
    reaction_type = models.CharField(max_length=1, choices=ReactionTypes.choices, default=ReactionTypes.LIKE)


class AnswerReaction(models.Model):
    class ReactionTypes(models.TextChoices):
        LIKE = "L", _("Like")
        DISLIKE = "D", _("Dislike")

    profile = models.ForeignKey(Profile, on_delete=models.PROTECT, related_name="answer_reactions")
    answer = models.ForeignKey(Answer, on_delete=models.PROTECT)
    reaction_type = models.CharField(max_length=1, choices=ReactionTypes.choices, default=ReactionTypes.LIKE)
