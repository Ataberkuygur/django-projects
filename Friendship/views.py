from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.http import JsonResponse
from User.models import CustomUser
from .models import Friendship

@login_required(login_url='User:login')
def send_request(request, slug):
    current_user = request.user
    to_user = get_object_or_404(CustomUser, username=slug)
    current_user_friends = current_user.friends.all()
    if to_user in current_user_friends:
        try:
            Friendship.objects.get(sender=request.user, receiver=to_user).delete()
        except:
            Friendship.objects.get(sender=to_user, receiver=request.user).delete()
    else:
        try:
            Friendship.objects.get(sender=request.user, receiver=to_user, status='send').delete()
        except:
            Friendship.objects.create(sender=request.user, receiver=to_user, status='send')
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

@login_required(login_url='User:login')
def accept_request(request, slug):
    sender = CustomUser.objects.get(username=slug)
    friendship = Friendship.objects.get(sender=sender, receiver=request.user, status='send')
    friendship.status = 'accepted'
    friendship.save()
    return redirect(request.META.get('HTTP_REFERER', 'redirect_if_referer_not_found'))

