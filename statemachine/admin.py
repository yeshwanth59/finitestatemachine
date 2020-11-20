
from django.contrib import admin

from statemachine.models import State, Question, Option, Workflow

import nested_admin


class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 1


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [OptionInline]
    extra = 1



@admin.register(State)
class StateAdmin(nested_admin.NestedPolymorphicInlineSupportMixin, nested_admin.NestedModelAdmin):
    inlines = (QuestionInline,)

@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass



