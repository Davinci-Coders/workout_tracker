from django import forms

from fitness.models import (Exercise, CardioExercise, Workout, ResistanceScheme, ResistanceSet,
                            CardioScheme, CardioDistance, CardioInterval, CardioRepetition)


class ExerciseForm(forms.ModelForm):
    class Meta:
        model = Exercise
        fields = ('title', 'body_part',)

class CardioExerciseForm(forms.ModelForm):
    class Meta:
        model = CardioExercise
        fields = ('title',)


class WorkoutForm(forms.ModelForm):
    class Meta:
        model = Workout
        fields = ('date', 'notes')


class ResistanceSchemeForm(forms.ModelForm):
    class Meta:
        model = ResistanceScheme
        fields = (
            'workout', 'exercise', 'modality', 'variation', 'rep_style',
            'notes'
        )


class ResistanceSetForm(forms.ModelForm):
    class Meta:
        model = ResistanceSet
        fields = (
            'scheme', 'reps', 'intensity', 'load'
        )


class CardioSchemeForm(forms.ModelForm):
    class Meta:
        model = CardioScheme
        fields = (
            'workout', 'exercise', 'modality', 'notes'
        )


class CardioDistanceForm(forms.ModelForm):
    class Meta:
        model = CardioDistance
        fields = (
            'scheme', 'start', 'stop', 'distance', 'measurement'
        )


class CardioIntervalForm(forms.ModelForm):
    class Meta:
        model = CardioInterval
        fields = (
            'scheme', 'action_start', 'action_stop', 'rest_start',
            'rest_stop', 'quantity',
        )


class CardioRepetitionForm(forms.ModelForm):
    class Meta:
        model = CardioRepetition
        fields = (
            'scheme', 'quantity', 'start', 'stop',
        )
