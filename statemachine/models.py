from django.contrib.auth.models import User
from django.db import models

from statemachine.enums import QuestionType


class Workflow(models.Model):
    name = models.CharField(max_length=32)

    def __str__(self):
        return self.name


class State(models.Model):
    name = models.CharField(max_length=32)
    condition = models.CharField(max_length=32, blank=True, null=True)
    initial_state = models.BooleanField(default=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)
    next_states = models.ManyToManyField('self', through='StateNextStates', symmetrical=False)
    terminal_state = models.BooleanField(default=False)

    def __str__(self):
        return self.name

    def validate(self, user_response):
        print(user_response)
        print(self.condition)
        if self.condition:
            return self.condition.lower() == user_response.lower()
        return True


class StateNextStates(models.Model):

    class Meta:
        ordering = ('priority_order',)

    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state_id')
    next_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='next_state')
    priority_order = models.PositiveIntegerField(default=0)


class Question(models.Model):
    question_type = models.IntegerField(choices=QuestionType.choices(), db_column='type', default=int(QuestionType.radio))
    question_text = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='questions')


class Option(models.Model):
    value = models.CharField(max_length=32)
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='options')


class User(models.Model):
    name = models.CharField(max_length=41)
    mobileNo = models.CharField(max_length=10)
    email = models.EmailField(max_length=20)
    pwd = models.CharField(max_length=10)
    image = models.ImageField(upload_to='upload/images', blank=True)
    address = models.CharField(max_length=100)


class UserState(models.Model):
    user_id = models.PositiveIntegerField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    workflow_id = models.PositiveIntegerField()
    pre_state_id = models.PositiveIntegerField(null=True, blank=True)
    option_id = models.PositiveIntegerField(null=True)


class UserStateMapping(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)




