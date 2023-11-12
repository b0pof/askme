from django.core.management import BaseCommand
from django.contrib.auth.models import User
from django.contrib.contenttypes.models import ContentType
from blog.models import Question, Answer, Profile, Tag, Reaction
from faker import Faker
from random import randint, choice
from django.utils import timezone
import datetime
# from pytz import UTC

fake = Faker()


class Command(BaseCommand):
    help = "Fills database with fake data"

    def add_arguments(self, parser):
        parser.add_argument("num", type=int)

    def handle(self, *args, **kwargs):
        ratio = kwargs['num']

        if ratio != None:
            try:
                ratio = int(ratio)
            except TypeError:
                return
        else:
            ratio = 10
        
        users_amount = ratio
        questions_amount = ratio * 10
        answers_amount = ratio * 100
        tags_amount = ratio
        actions_amount = ratio * 200

        # USERS

        users = []

        for _ in range(users_amount):
            users.append(
                User(
                    email=fake.email(),
                    username=fake.user_name(),
                    password=str(fake.password()),
                    date_joined=timezone.now() + datetime.timedelta(seconds=randint(0, 31536000))
                )
            )
        
        User.objects.bulk_create(users)

        current_users = User.objects.all()
        u_amount = current_users.count()

        profiles = []
        for i in range(users_amount):
            profiles.append(
                Profile(
                    user=current_users[u_amount - len(users) + i],
                    rating=str(randint(0, 135))
                )
            )

        Profile.objects.bulk_create(profiles) 

        # TAGS

        tags = [
            Tag(
                word=fake.word()
            ) for _ in range(tags_amount)
        ]

        Tag.objects.bulk_create(tags)
        
        # QUESTIONS

        current_profiles = Profile.objects.all()
        p_amount = current_profiles.count() 

        questions = []

        for i in range(questions_amount):
            questions.append(
                Question(
                    title=fake.sentence(8),
                    description = fake.sentence(randint(30, 100)),
                    author=current_profiles[randint(p_amount - users_amount, p_amount - 1)],
                    creation_date=timezone.now() + datetime.timedelta(seconds=randint(0, 31536000))
                )
            )
        
        Question.objects.bulk_create(questions)

        # TAGS FOR QUESTIONS

        current_questions = Question.objects.all()
        q_amount = current_questions.count() 

        for i in range(questions_amount):
            for _ in range(randint(1, 4)):
                current_questions[q_amount - questions_amount + i].tags.add(tags[randint(1, tags_amount - 1)])

        # REACTIONS FOR QUESTIONS

        model_type = ContentType.objects.get_for_model(current_questions[0])

        q_reactions = []

        for i in range(questions_amount):
            for _ in range(randint(5, 25)):
                q_reactions.append(
                    Reaction(
                        content_type=model_type,
                        object_id=current_questions[q_amount - questions_amount + i].id,
                        profile=current_profiles[randint(p_amount - users_amount, p_amount - 1)],
                        reaction_type = choice(["L", "L", "D"])
                    )
                )
        
        Reaction.objects.bulk_create(q_reactions)

        # ANSWERS

        answers = []

        for _ in range(answers_amount):
            answers.append(
                Answer(
                    question=current_questions[randint(1, q_amount - 1)],
                    description=fake.sentence(randint(20, 50)),
                    author=current_profiles[randint(1, p_amount - 1)],
                    is_correct=randint(0, 1),
                    creation_date=timezone.now() + datetime.timedelta(seconds=randint(0, 31536000))
                )
            )
        
        Answer.objects.bulk_create(answers)

        # REACTIONS FOR ANSWERS

        current_answers = Answer.objects.all()
        a_amount = current_answers.count()

        model_type = ContentType.objects.get_for_model(current_answers[0])

        a_reactions = []

        for i in range(answers_amount):
            for _ in range(randint(2, 5)):
                a_reactions.append(
                    Reaction(
                        content_type=model_type,
                        object_id=current_answers[a_amount - answers_amount + i].id,
                        profile=current_profiles[randint(p_amount - users_amount, p_amount - 1)],
                        reaction_type = choice(["L", "L", "L", "D", "D"])
                    )
                )
        
        Reaction.objects.bulk_create(a_reactions)
