from django.conf.urls import url

from fitness.views import home, exercise, resistance_exercise_form, cardio_exercise_form, new_cardio_distance, new_cardio_interval, new_cardio_repetition, new_cardio_scheme, NewWorkoutView, single_workout, ResistanceSchemeView, ResistanceSetView

urlpatterns = [
    url(r'^workout/(?P<workout_id>[0-9]+)$', single_workout, name='single_workout'),
    url(r'^exercise', exercise, name='exercise'),
    url(r'^new_resistance_exercise', resistance_exercise_form, name='resistance_exercise_form'),
    url(r'^new_cardio_exercise', cardio_exercise_form, name='cardio_exercise_form'),
    url(r'^new_workout$', NewWorkoutView.as_view(), name='new_workout'),
    url(r'^new_resistance_scheme/(?P<workout_id>[0-9]+)$', ResistanceSchemeView.as_view(),
        name='new_resistance_scheme'),
    url(r'^new_resistance_set/(?P<scheme_id>[0-9]+)$', ResistanceSetView.as_view(), name='new_resistance_set'),
    # url(r'^new_workout_set/(?P<workout_id>[0-9]+)$', NewWorkoutSetView.as_view(), name='new_workout_set'),
    url(r'^new_cardio_scheme/(?P<workout_id>[0-9]+)$', new_cardio_scheme, name='new_cardio_scheme'),
    url(r'^new_cardio_interval/(?P<scheme_id>[0-9]+)$', new_cardio_interval, name='new_cardio_interval'),
    url(r'^new_cardio_repetition/(?P<scheme_id>[0-9]+)$', new_cardio_repetition, name='new_cardio_repetition'),
    url(r'^new_cardio_distance/(?P<scheme_id>[0-9]+)$', new_cardio_distance, name='new_cardio_distance'),
    url(r'^$', home, name='home'),
]
