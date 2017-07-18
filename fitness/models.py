# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from datetime import datetime

from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone


REP_STYLE_CHOICES = (
    ('str', 'Strength'),
    ('hypertrophy', 'Hypertrophy'),
    ('power', 'Power'),
    ('endurance', 'Endurance'),
)


BODY_PART_CHOICES = (
    ('arms', 'Arms'),
    ('legs', 'Legs'),
    ('chest', 'Chest'),
    ('back', 'Back'),
    ('shoulder', 'Shoulder'),
    ('core', 'Core'),
)


MODALITY_CHOICES = (
    ('barbell', 'Barbell'),
    ('kettlebell', 'Kettlebell'),
    ('dumbbell', 'Dumbbell'),
    ('machine', 'Machine'),
    ('cable', 'Cable'),
    ('smith', 'Smith'),
    ('band', 'Band'),
    ('body-weight', 'Body Weight'),
)

CARDIO_MODALITY_CHOICES = (

)


class Exercise(models.Model):
    title = models.CharField(max_length=200)
    body_part = models.CharField(max_length=50, choices=BODY_PART_CHOICES)
   
    def __str__(self):
        return self.title

class CardioExercise(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Workout(models.Model):
    date = models.DateField(default=timezone.now)
    user = models.ForeignKey(User)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return '{} on {}'.format(self.user.username, datetime.strftime(self.date, '%m-%d-%Y'))


class WorkoutScheme(models.Model):
    variation = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)

    class Meta:
        abstract = True


class ResistanceScheme(models.Model):
    workout = models.ForeignKey(Workout, related_name='resistance_scheme')
    exercise = models.ForeignKey(Exercise)
    variation = models.CharField(max_length=100, blank=True, null=True)
    notes = models.TextField(null=True, blank=True)
    rep_style = models.CharField(max_length=20, blank=True, null=True, choices=REP_STYLE_CHOICES)
    modality = models.CharField(max_length=50, blank=True, null=True, help_text='Method of exercise',
                                choices=MODALITY_CHOICES)

    def __str__(self):
        return '{} - {}'.format(datetime.strftime(self.workout.date, '%m-%d-%Y'),
                                self.exercise)


class ResistanceSet(models.Model):
    scheme = models.ForeignKey(ResistanceScheme, related_name='resistance_set')
    reps = models.IntegerField()
    intensity = models.IntegerField()
    load = models.IntegerField(help_text='Weight in pounds')

    @property
    def work(self):
        if self.reps <= 12:
            return int((self.reps * self.load * .033) + self.load)
        else:
            return 'too many reps to calculate'

    def set_rep_style(self):
        if self.reps > 0 and self.reps <= 5:
            return 'Strength/Power'
        if self.reps > 5 and self.reps <= 12:
            return 'Hypertrophy'
        if self.reps > 12:
            return 'Endurance'

    def __str__(self):
        return '{}@{}lbs'.format(self.reps, self.load)


class CardioScheme(WorkoutScheme):
    workout = models.ForeignKey(Workout, related_name='cardio_scheme')
    exercise = models.ForeignKey(CardioExercise)
    modality = models.CharField(max_length=50, blank=True, null=True, help_text='Method of cardio',
                                choices=CARDIO_MODALITY_CHOICES)

    def __str__(self):
        return '{} - {}'.format(datetime.strftime(self.workout.date, '%m-%d-%Y'),
                                self.exercise)


class CardioDistance(models.Model):
    scheme = models.ForeignKey(CardioScheme, related_name='distance_set')
    start = models.TimeField(blank=True, null=True)
    stop = models.TimeField(blank=True, null=True)
    distance = models.FloatField()
    # TODO: add choices for measurement field
    measurement = models.CharField(max_length=200)

    @property
    def time_seconds(self):
        if self.start and self.stop:
            time_delta = datetime.combine(datetime.today(), self.stop) - \
                         datetime.combine(datetime.today(), self.start)
            return time_delta.seconds
        return 0

    def __str__(self):
        return '{} in {} seconds'.format(self.time_seconds, self.distance) # maybe needs to change


# obj = CardioInterval.objects.first()
# obj.action_time_seconds  # calling as a property

class CardioInterval(models.Model):
    scheme = models.ForeignKey(CardioScheme, related_name='interval_set')
    action_start = models.TimeField(blank=True, null=True)
    action_stop = models.TimeField(blank=True, null=True)
    rest_start = models.TimeField(blank=True, null=True)
    rest_stop = models.TimeField(blank=True, null=True)
    quantity = models.IntegerField(default=1)

    @property
    def action_time_seconds(self):
        if self.action_start and self.action_stop:
            action_time_delta = datetime.combine(datetime.today(), self.action_stop) - \
                                datetime.combine(datetime.today(), self.action_start)
            return action_time_delta.seconds
        return 0

    @property
    def rest_time_seconds(self):
        if self.rest_start and self.rest_stop:
            rest_time_delta = datetime.combine(datetime.today(), self.rest_stop) - \
                              datetime.combine(datetime.today(), self.rest_start)
            return rest_time_delta.seconds
        return 0

    def save(self, force_insert=False, force_update=False, using=None, update_fields=None):
        my_dict = {'a': 'aa', 'b': 'bb', }
        # dict.get('VAR_NAME', 'DEFAULT_VALUE')
        my_dict.get('c', 'there is no c')
        # getattr(INSTANCE, 'VAR_NAME', DEFAULT_VALUE)
        # if getattr(self, 'action_time', False):
            # import ipdb
            # ipdb.set_trace()
        super(CardioInterval, self).save(force_insert, force_update, using, update_fields)

    def __str__(self):
        return 'action: {}, rest: {}, units: {}'.format(self.action_time_seconds, self, rest_time_seconds, self.quantity)


class CardioRepetition(models.Model):
    scheme = models.ForeignKey(CardioScheme, related_name='repetition_set')
    quantity = models.IntegerField()
    start = models.TimeField(blank=True, null=True)
    stop = models.TimeField(blank=True, null=True)

    @property
    def time_seconds(self):
        if self.start and self.stop:
            time_delta = datetime.combine(datetime.today(), self.stop) - \
                         datetime.combine(datetime.today(), self.start)
            return time_delta.seconds
        return 0

    def __str__(self):
        return '{} in {}'.format(self.quantity, self.time_seconds)
