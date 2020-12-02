from django.contrib.auth.models import User
from django.db import models


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

    def __str__(self):
        return self.name

    def validate(self, user_response):
        print(user_response)
        print(self.condition)
        return self.condition.lower() == user_response.lower()


class StateNextStates(models.Model):

    class Meta:
        ordering = ('priority_order',)

    state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='state_id')
    next_state = models.ForeignKey(State, on_delete=models.CASCADE, related_name='next_state')
    priority_order = models.PositiveIntegerField(default=0)


class Question(models.Model):
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


class UserState(models.Model):
    user_id = models.PositiveIntegerField()
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    workflow_id = models.PositiveIntegerField()


class UserStateMapping(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


