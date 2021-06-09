from django.contrib.auth.decorators import login_required
from Group.models import Group
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError
from django.contrib import messages
from User.models import CustomUser
from Task.models import Category

@login_required(login_url='User:login')
def Explore(request):
    #Kullanıcıları Göster
    user_input = request.GET.get('user_input')
    group_input = request.GET.get('group_input')
    user_input = str(user_input)
    group_input = str(group_input)
    groups = Group.objects.filter(name__icontains=group_input)
    print(groups)
    users = CustomUser.objects.filter(username__icontains=user_input).exclude(username=request.user.username)
    context = {
        'users': users,
        'groups': groups,
    }
    return render(request, 'other_templates/explore.html', context)

@login_required(login_url='User:login')
def Settings(request, slug):
    if slug == request.user.username.replace('ı','i'):
        category_list = Category.objects.filter(user=request.user)
        return render(request, 'other_templates/settings.html', {'category_list': category_list})
    else:
        return HttpResponseForbidden()


@login_required(login_url='User:login')
def Notifications(request, slug):
    return render(request, 'other_templates/notifications.html')


@login_required(login_url='User:login')
def CategoryCreate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            if len(request.user.category_set.all()) == 8:
                raise ValidationError('En fazla 8 kategori oluşturabilirsin!')
            print(len(request.user.category_set.all()))
            category = request.POST.get('category', None)                
            priority = request.POST.get('priority', None)
            if (len(category) < 1):
                raise ValidationError('Yazı girmelisiniz!')
            elif (len(category) > 20):
                raise ValidationError('20 Karakterden fazla giremezsiniz!')
            elif (len(category.split()) > 2):
                raise ValidationError('Maximum 2 Kelime yazabilirsiniz!')
            new_category = Category.objects.create(title = category, priority = priority, user=request.user)
            new_category.save()
            messages.success(request, 'Yeni Kategori Eklendi')
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='User:login')
def CategoryDelete(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            selected_category = request.POST.get('selected_category', None)
            if selected_category != None:
                category = get_object_or_404(Category, title=selected_category, user=request.user)
                category.delete()
            return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='User:login')
def CategoryListDelete(request):
    if request.user.is_authenticated:
        Category.objects.filter(user=request.user).delete()
        messages.warning(request, 'Tüm kategoriler silindi!')
        return redirect('Task:index')
    else:
        return HttpResponseForbidden

@login_required(login_url='User:login')
def GoalCreate(request):
    if request.user.is_authenticated:
        if request.method == "POST":
            new_goal = request.POST.get('goal', None)
            if (int(new_goal) < 1):
                raise ValidationError('Sayı girmelisiniz!')
            request.user.goal_score = new_goal
            request.user.save()
            messages.info(request, 'Yeni hedef!')
            return redirect('Task:index')