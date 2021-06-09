from django.contrib.auth.decorators import login_required
from django.core.exceptions import ValidationError
from django.http.response import JsonResponse
from .models import Pomodoro
from django.shortcuts import get_object_or_404, render, redirect
import datetime

@login_required(login_url='User:login')
def PomodoroSettings(request):
    if request.method == "POST":
        Pomodoro.objects.filter(user=request.user).delete()
        title = request.POST.get('title_input', None)
        minute = request.POST.get('minute_input', None)
        seconds = request.POST.get('second_input', None)
        rest_minute = request.POST.get('rest_m_input', None)
        rest_seconds = request.POST.get('rest_s_input', None)
        pomodoro_time = Pomodoro.objects.create(user=request.user)
        if (len(title) > 14):
            raise ValidationError('12 Karakterden Fazla Yazamazsın!')
        pomodoro_time.title = title
        pomodoro_time.minutes = minute
        pomodoro_time.seconds = seconds
        pomodoro_time.rest_minutes = rest_minute
        pomodoro_time.rest_seconds = rest_seconds
        pomodoro_time.save()
        return redirect('Pomodoro:timer')
    else:
        print('anan')
        return render(request, 'pomodoro/pomodoro_settings.html')

@login_required(login_url='User:login')
def PomodoroTimer(request):
    pomodoro_timer = get_object_or_404(Pomodoro, user=request.user)
    title = pomodoro_timer.title
    minutes = pomodoro_timer.minutes
    seconds = pomodoro_timer.seconds
    rest_minutes = pomodoro_timer.rest_minutes
    rest_seconds = pomodoro_timer.rest_seconds
    context = {
        'title': title,
        'minutes': minutes,
        'seconds': seconds,
        'rest_minutes': rest_minutes,
        'rest_seconds': rest_seconds,
    }
    return render(request, 'pomodoro/pomodoro_timer.html', context)