from django.contrib.auth.models import User
from django.db import models


class Workflow(models.Model):
    name = models.CharField(max_length=32)


class State(models.Model):
    name = models.CharField(max_length=32)
    condition = models.CharField(max_length=32, blank=True, null=True)
    initial_state = models.BooleanField(default=False)
    workflow = models.ForeignKey(Workflow, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Question(models.Model):
    question_text = models.CharField(max_length=100)
    state = models.ForeignKey(State, on_delete=models.CASCADE)


class Option(models.Model):
    value = models.CharField(max_length=32)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)


class UserStateMapping(models.Model):
    state = models.ForeignKey(State, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)


