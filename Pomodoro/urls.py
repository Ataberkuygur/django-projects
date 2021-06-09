from django.urls import path
from .views import PomodoroSettings, PomodoroTimer

app_name = 'Pomodoro'

urlpatterns = [
    path("timer/", PomodoroTimer, name="timer"),
    path("settings/", PomodoroSettings, name="settings"),
]

