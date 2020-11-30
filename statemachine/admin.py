
from django.contrib import admin

from statemachine.models import State, Question, Option, Workflow
from adminsortable2.admin import SortableInlineAdminMixin

import nested_admin


class OptionInline(nested_admin.NestedTabularInline):
    model = Option
    extra = 1


class QuestionInline(nested_admin.NestedTabularInline):
    model = Question
    inlines = [OptionInline]
    extra = 1


class StateTabularInline(SortableInlineAdminMixin, admin.TabularInline):
    model = State.next_states.through
    fk_name = 'state'
    extra = 0


@admin.register(State)
class StateAdmin(nested_admin.NestedPolymorphicInlineSupportMixin, nested_admin.NestedModelAdmin):
    inlines = (StateTabularInline, QuestionInline )


@admin.register(Workflow)
class WorkflowAdmin(admin.ModelAdmin):
    pass


