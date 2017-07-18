# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import admin

from fitness.models import Exercise, CardioExercise, Workout, ResistanceScheme, ResistanceSet, CardioScheme, CardioDistance, CardioRepetition, CardioInterval


admin.site.register(Exercise)
admin.site.register(CardioExercise)

admin.site.register(CardioScheme)
admin.site.register(CardioInterval)
admin.site.register(CardioRepetition)
admin.site.register(CardioDistance)


class ResistanceSetInline(admin.StackedInline):
    model = ResistanceSet


@admin.register(ResistanceScheme)
class ResistanceSchemeAdmin(admin.ModelAdmin):
    inlines = (ResistanceSetInline, )


class ResistanceSchemeInline(admin.StackedInline):
    model = ResistanceScheme


@admin.register(Workout)
class WorkoutAdmin(admin.ModelAdmin):
    inlines = (ResistanceSchemeInline, )
