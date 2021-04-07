from django.shortcuts import render
from django.http import HttpResponse
from .models import Setting

def index(request):
    setting = Setting.objects.get()

    context = {
        'setting': setting,
    }
    return render(request, 'index.html', context)
