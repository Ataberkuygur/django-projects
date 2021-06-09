from django.shortcuts import get_object_or_404, render, redirect
from django.core.exceptions import ValidationError
from .models import Addiction
from .forms import AddictionForm
import datetime

def AddictionIndex(request):
    context = dict()
    context['form'] = AddictionForm()
    addictions = Addiction.objects.filter(user=request.user)
    context['addictions'] = addictions
    if request.method == "POST":
        if len(addictions) < 5:
            form = AddictionForm(request.POST or None)
            if form.is_valid():
                new_addiction = form.save(commit=False)
                new_addiction.user = request.user
                new_addiction.save()
                return redirect('Addiction:index')
            else:
                return render(request, 'addiction/index.html', context)
        else:
            raise ValidationError("4'ten fazla oluşturamazsın!")
    else:
        return render(request, 'addiction/index.html', context)

def AddictionDetail(request, slug):
    context = dict()
    addiction = get_object_or_404(Addiction, slug=slug)
    addiction.day = int(datetime.datetime.now().day) - int(addiction.created_date.day)
    addiction.week = (int(datetime.datetime.now().day) - int(addiction.created_date.day)) // 7
    addiction.month = (int(datetime.datetime.now().day) - int(addiction.created_date.day)) // 30
    addiction.save()
    if addiction.day == 3:
        request.user.score += 10
    if addiction.week == 2:
        request.user.score += 15
    if addiction.month == 1:
        request.user.score += 20
    if addiction.month == 6:
        request.user.score += 40
    if addiction.month == 12:
        request.user.score += 60
    request.user.save()
    addiction_day = addiction.day
    addiction_week = addiction.week
    addiction_month = addiction.month
    context['addiction'] = addiction
    context['addiction_day'] = addiction_day
    context['addiction_week'] = addiction_week
    context['addiction_month'] = addiction_month
    return render(request, 'addiction/detail.html', context)