from django.contrib.auth import authenticate, login
from django.contrib.auth.decorators import login_required
from django.forms import ValidationError
from django.http.response import HttpResponseForbidden, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib import messages
from .models import CustomUser, Profile
from .forms import CustomUserCreationForm, CustomUserUpdateForm
from Friendship.models import Friendship

def RegisterCustomUser(request):
    form = CustomUserCreationForm()
    if request.method == "POST":
        form = CustomUserCreationForm(request.POST or None, request.FILES or None)
        if form.is_valid:
            form.save()
            messages.success(request, 'Başarıyla kayıt oldunuz!')
            return redirect('User:login')
        else:
            return render(request, 'registration/register_custom_user.html', {'form': form})
    else:
        return render(request, 'registration/register_custom_user.html', {'form': form})

def CustomUserLogin(request):
    if request.method == "POST":    
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('Task:index')
        else:
            error_message = 'Geçersiz giriş!'
            return render(request, 'registration/login.html', {'error_message': error_message})
    else:
        return render(request, 'registration/login.html')

@login_required(login_url='User:login')
def UpdateCustomUser(request, slug):
    if request.user.is_authenticated:
        if request.user.username == slug:
            the_user = get_object_or_404(CustomUser, username=slug)
            form = CustomUserUpdateForm(instance=the_user)
            if request.method == "POST":
                form = CustomUserUpdateForm(request.POST or None, request.FILES or None)
                if form.is_valid():
                    form.save()
                    messages.success(request, 'Kullanıcıyı başarıyla güncellediniz!')
                    return HttpResponseRedirect(the_user.profile_set.get().get_absolute_url())
                else:
                    return render(request, 'registration/update_custom_user.html', {'form': form})
            else:
                return render(request, 'registration/update_custom_user.html', {'form': form})
        else:
            return HttpResponseForbidden()

@login_required(login_url='User:login')
def CustomUserProfile(request, slug):
    current_user = request.user
    customUserProfile = get_object_or_404(Profile, slug=slug)
    if slug == request.user.username:
        total_score = current_user.get_day_score()
        context = {
            'profile': customUserProfile, 
            'total_score': total_score
        }
        return render(request, 'user/profile.html', context)
    else:
        try:
            friendship = Friendship.objects.get(sender=request.user, receiver=customUserProfile.user)
        except:
            friendship = ''
        context = {
            'profile': customUserProfile, 
            'friendship': friendship,
        }
        return render(request, 'user/profile.html', context)


    
    

