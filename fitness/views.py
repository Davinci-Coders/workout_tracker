# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.contrib import messages
from django.core.urlresolvers import reverse
from django.forms import formset_factory
from django.shortcuts import redirect, render
from django.views import View

from fitness.forms import CardioDistanceForm, CardioRepetitionForm, CardioIntervalForm, CardioSchemeForm, ResistanceSetForm, ResistanceSchemeForm, WorkoutForm
from fitness.models import CardioScheme, ResistanceScheme, Workout


def account_settings(request):
    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))
    context = {
    }
    return render(request, 'account_settings.html', context)


def home(request):
    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))

    context = {
        'workouts': Workout.objects.filter(user=request.user),
    }
    return render(request, 'home.html', context)


def single_workout(request, workout_id):
    if not request.user.is_authenticated:
        return redirect(reverse('account_login'))

    # TODO: handle case where no workout with id found or invalid user
    try:
        workout = Workout.objects.get(user=request.user, id=workout_id)
    except Workout.DoesNotExist:
        messages.add_message(request, messages.ERROR, 'No horkout with id {}.'.format(workout_id))
        return redirect(reverse('home'))
    context = {
        'workout': workout,
    }
    return render(request, 'fitness/single.html', context)


class NewWorkoutView(View):
    def get(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))
        context = {
            'form': WorkoutForm,
        }
        return render(request, 'fitness/new_workout.html', context)

    def post(self, request):
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))
        form = WorkoutForm(request.POST)
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'fitness/new_workout.html', context)
        # next 3 lines are largely equivalent
        # workout_obj = Workout(date='TODAYS DATE', notes='notes from user')
        # workout_obj = Workout(date=request.POST.get('date'), notes=request.POST.get('notes'))
        workout_obj = form.save(commit=False)
        workout_obj.user = request.user
        workout_obj.save()

        if request.POST.get('resist'):
            return redirect(reverse('new_resistance_scheme', kwargs={'workout_id': workout_obj.id}))
        elif request.POST.get('cardio'):
            return redirect(reverse('new_cardio_scheme', kwargs={'workout_id': workout_obj.id}))
        else:
            messages.warning(request, 'Resistance is futile?')
            return redirect(reverse('home'))


# Resistance #

class ResistanceSchemeView(View):
    def get(self, request, workout_id):
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))
        try:
            workout = Workout.objects.get(user=request.user, id=workout_id)
        except Workout.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No horkout with id {}.'.format(workout_id))
            return redirect(reverse('home'))
        context = {
            'form': ResistanceSchemeForm(initial={'workout': workout}),
        }
        return render(request, 'fitness/new_workout_scheme.html', context)

    def post(self, request, workout_id):
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))
        try:
            workout = Workout.objects.get(user=request.user, id=workout_id)
        except Workout.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No horkout with id {}.'.format(workout_id))
            return redirect(reverse('home'))
        form = ResistanceSchemeForm(request.POST, initial={'workout': workout})
        if not form.is_valid():
            context = {
                'form': form,
            }
            return render(request, 'fitness/new_workout_scheme.html', context)
        scheme = form.save()

        if request.POST.get('num_sets'):
            num_sets = request.POST.get('num_sets')
            try:
                num_sets = int(num_sets)
                return redirect('{}?num_sets={}'.format(
                    reverse('new_resistance_set', kwargs={'scheme_id': scheme.id}),
                    num_sets))
            except TypeError:
                pass

        return redirect(reverse('new_resistance_set', kwargs={'scheme_id': scheme.id}))


class ResistanceSetView(View):
    form_set = formset_factory(ResistanceSetForm, extra=2)

    def get(self, request, scheme_id):
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))

        num_sets = request.GET.get('num_sets', False)
        if num_sets:
            try:
                num_sets = int(num_sets)
                self.form_set = formset_factory(ResistanceSetForm, extra=num_sets-1)
            except TypeError:
                pass

        try:
            scheme = ResistanceScheme.objects.get(workout__user=request.user, id=scheme_id)
        except ResistanceScheme.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No ResistanceScheme with id {}.'.format(scheme_id))
            return redirect(reverse('home'))
        context = {
            # 'form_set': form_set(),
            'form_set': self.form_set(initial=[{'scheme': scheme}, ]),
        }
        return render(request, 'fitness/new_resistance_set.html', context)

    def post(self, request, scheme_id):
        if not request.user.is_authenticated:
            return redirect(reverse('account_login'))
        try:
            scheme = ResistanceScheme.objects.get(workout__user=request.user, id=scheme_id)
        except ResistanceScheme.DoesNotExist:
            messages.add_message(request, messages.ERROR, 'No ResistanceScheme with id {}.'.format(scheme_id))
            return redirect(reverse('home'))
        form_set = self.form_set(request.POST)
        # form_set = self.form_set(request.POST, initial=[{'scheme': scheme}, ])
        # form = ResistanceSetForm(request.POST, initial={'scheme': scheme})
        if not form_set.is_valid():
            context = {
                'form_set': form_set,
            }
            return render(request, 'fitness/new_resistance_set.html', context)
        for form in form_set.forms:
            workout_set = form.save()

        if request.POST.get('add_another'):
            # return self.get(request, workout_id)
            return redirect((reverse('new_resistance_set', kwargs={'scheme_id': scheme.id})))

        if request.POST.get('save_review'):
            # return self.get(request, workout_id)
            return redirect((reverse('single_workout', kwargs={'workout_id': workout_set.scheme.workout.id})))

        # add another workout set?

        return redirect(reverse('new_resistance_scheme', kwargs={'workout_id': workout_set.scheme.workout.id}))


# Cardio #

def new_cardio_scheme(request, workout_id):
    workout = Workout.objects.get(user=request.user, id=workout_id)
    form = CardioSchemeForm(initial={'workout': workout})
    if request.method == 'POST':
        form = CardioSchemeForm(request.POST, initial={'workout': workout})
        if form.is_valid():
            scheme = form.save()
            if request.POST.get('cardio_interval'):
                return redirect(reverse('new_cardio_interval', kwargs={'scheme_id': scheme.id}))
            elif request.POST.get('cardio_repetition'):
                return redirect(reverse('new_cardio_repetition', kwargs={'scheme_id': scheme.id}))
            elif request.POST.get('cardio_distance'):
                return redirect(reverse('new_cardio_distance', kwargs={'scheme_id': scheme.id}))
            else:
                messages.success(request, 'New Cardio Scheme Saved')
                return redirect(reverse('single_workout', kwargs={'workout_id': workout_id}))

    context = {
        'form': form,
    }
    return render(request, 'fitness/new_cardio_scheme.html', context)


# def new_cardio_scheme(request, workout_id):
#     if not request.user.is_authenticated:
#         return redirect(reverse('account_login'))
#     try:
#         workout = Workout.objects.get(user=request.user, id=workout_id)
#     except Workout.DoesNotExist:
#         messages.add_message(request, messages.ERROR, 'No horkout with id {}.'.format(workout_id))
#         return redirect(reverse('home'))
#     form = CardioSchemeForm(initial={'workout': workout}),
#     if request.method == 'POST':
#         form = CardioSchemeForm(request.POST, initial={'workout': workout})
#         if form.is_valid():
#             scheme = form.save()
#             # TODO : handle create set step
#
#     context = {
#         'form': form
#     }
#     return render(request, 'fitness/new_cardio_scheme.html', context)
#
#
def new_cardio_interval(request, scheme_id):
    scheme = CardioScheme.objects.get(workout__user=request.user, id=scheme_id)
    form = CardioIntervalForm(initial={'scheme': scheme})
    if request.method == 'POST':
        form = CardioIntervalForm(request.POST, initial={'scheme': scheme})
        if form.is_valid():
            form.save()
            messages.success(request, 'You saved it')
            if request.POST.get('add_another'):
                url = reverse('new_cardio_interval', kwargs={'scheme_id': scheme.id})
            elif request.POST.get('add_scheme'):
                url = reverse('new_cardio_scheme', kwargs={'workout_id': scheme.workout.id})
            elif request.POST.get('add_resistance'):
                url = reverse('new_resistance_scheme', kwargs={'workout_id': scheme.workout.id})
            else:
                url = reverse('single_workout', kwargs={'workout_id': scheme.workout.id})
            return redirect(url)
    context = {
        'form': form,
    }
    return render(request, 'fitness/new_cardio_interval.html', context)


def new_cardio_repetition(request, scheme_id):
    scheme = CardioScheme.objects.get(workout__user=request.user, id=scheme_id)
    form = CardioRepetitionForm(initial={'scheme': scheme})
    if request.method == 'POST':
        form = CardioRepetitionForm(request.POST, initial={'scheme': scheme})
        if form.is_valid():
            form.save()
            # TODO: do something with user from here
            messages.success(request, 'You saved it')
    context = {
        'form': form,
    }
    return render(request, 'fitness/new_cardio_repetition.html', context)


def new_cardio_distance(request, scheme_id):
    scheme = CardioScheme.objects.get(workout__user=request.user, id=scheme_id)
    form = CardioDistanceForm(initial={'scheme': scheme})
    if request.method == 'POST':
        form = CardioDistanceForm(request.POST, initial={'scheme': scheme})
        if form.is_valid():
            form.save()
            # TODO: do something with user from here
            messages.success(request, 'You saved it')
    context = {
        'form': form,
    }
    return render(request, 'fitness/new_cardio_distance.html', context)





    