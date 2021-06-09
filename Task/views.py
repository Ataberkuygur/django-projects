from django.contrib.auth import login
from django.core.exceptions import ValidationError
from django.http.response import HttpResponseBadRequest, HttpResponseRedirect, JsonResponse, HttpResponseForbidden
from django.shortcuts import get_list_or_404, get_object_or_404, render, redirect
from django.contrib import messages
from django.http import HttpResponse
from django.core.mail import send_mail
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from Friendship.models import Friendship
from User.models import CustomUser
from .models import Category, Task
import datetime

def TaskIndex(request):
    if not request.user.is_authenticated:
        return render(request, 'task/index.html')
    else:        
        #Kullanıcıya Ait Görevler
        current_user = request.user
        total_score = 0
        task_list = current_user.task_set.all()
        #Görevin süresinin üzerinden 24 saat geçince kendisini silmesi
        for task in task_list:
            if datetime.datetime.now().day == task.created_time.day+1:
                task.delete()
                return redirect('Task:index')
                 
        #Her Sayfada 6 Max. Görev Gösterme       
        paginator = Paginator(task_list, 5)
        page_number = request.GET.get('page')
        page_obj = paginator.get_page(page_number)

        #Günlük Puanı Getirir
        total_score = current_user.get_day_score()
        
        #Kullanıcıya ait kategorileri gösterme
        category_list = Category.objects.filter(user=request.user)
        context = {
            'page_obj': page_obj,
            'total_score': total_score,
            'category_list': category_list,
        }
        return render(request, 'task/index.html', context)


@login_required(login_url='User:login')
def TaskCreate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            title = request.POST.get('title', None)
            category = request.POST.get('category', None)
            done = request.POST.get('done', None)
            if (title != None and title != '') and (done != None and done != '') and (category != None and category != ''):
                raise ValidationError('Boş bırakılamaz!')
            if done == 'on':
                done = True
            else:
                done = False

            #Başlık 66 Karakterden Fazla Olursa Hata Vermesi
            if len(title) > 66:
                raise ValidationError('66 karakterden fazla yazamazsın!')
            if category == None:
                new_task = Task.objects.create(title = title, done = done, user = request.user)
            else:
                category = Category.objects.get(user=request.user, title=category)
                new_task = Task.objects.create(title = title, done = done, category=category, user = request.user)
            
            #Önem Derecesine Göre Renk Atama
            messages.info(request, 'Görevi oluşturdun! Bitir, puan kazan ve hedefine yaklaş!')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseForbidden()
        
@login_required(login_url='User:login')
def TaskUpdate(request, slug):
    task = get_object_or_404(Task, slug = slug)
    if task.user == request.user:
        if request.method == "POST":
            title_update = request.POST.get('title_update', None)
            done_update = request.POST.get('done_update', None)
            category_update = request.POST.get('category_update', None)
            if done_update != None:
                done_update = True
            else:
                done_update = False   
            if len(title_update) > 66:
                raise ValidationError('66 karakterden fazla yazamazsın!')
            task.title = title_update
            task.done = done_update
            if category_update == None:
                task.category = None
            else:
                category_update = Category.objects.get(user=request.user, title__icontains=category_update)
                task.category = category_update
            task.save()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
        else:
            update_category_list = Category.objects.all()
            print(update_category_list)
            if task.category in update_category_list:
                update_category_list = Category.objects.all().exclude(task.category)
            print(update_category_list)
            return JsonResponse(update_category_list, safe=False)
    else:
        return HttpResponseForbidden()

@login_required(login_url='User:login')
def TaskDelete(request, slug):
    task = get_object_or_404(Task, slug=slug)
    if task.user == request.user:
        task.delete()
    else:
        return HttpResponseForbidden()
    return JsonResponse('Deleted!', safe=False)

@login_required(login_url='User:login')
def TaskListDelete(request, slug):
    if request.user.username == slug:
        current_user = request.user
        task_list = Task.objects.filter(user=current_user)
        task_list.delete()
        return redirect('Task:index')
    else:
        return HttpResponseForbidden()

@login_required(login_url='User:login')
def Done_or_Not(request, slug):
    task = get_object_or_404(Task, slug=slug)
    if task.user == request.user:
        task_title = ''
        if task.done == True:
            task.done = False
        else:
            task.done = True
        task.save()
        return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))
    else:
        return HttpResponseForbidden()
