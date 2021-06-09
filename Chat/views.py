from django.contrib.auth.decorators import login_required
from django.http.response import HttpResponseForbidden
from django.shortcuts import render, redirect
from django.db.models import Q
from django.contrib.auth import login
from User.models import CustomUser
from .models import Room, Message

@login_required(login_url='User:login')
def index(request):
    if not request.user.is_authenticated:
        return redirect('User:login')
    user_list = request.user.friends.all()
    rooms = Room.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
    room_message_list = []
    room_message_owners = []
    for room in rooms:
        room_message_list = Message.objects.filter(room=room, is_seen=False).exclude(user=request.user)
        for room_message in room_message_list:
            if room_message.user in room_message_owners:
                pass
            else:
                room_message_owners.append(room_message.user)
    return render(request, 'chat/index.html', {'user_list': user_list, 'room_message_owners': room_message_owners})

@login_required(login_url='User:login')
def start_chat(request, second_user):
    if not request.user.is_authenticated:
        return redirect('User:login')    
    second_user = CustomUser.objects.get(username=second_user)
    print(second_user)
    try:
        room = Room.objects.get(first_user=request.user, second_user=second_user)
    except Room.DoesNotExist:
        try:
            room = Room.objects.get(second_user=request.user, first_user=second_user)
        except:
            room = Room.objects.create(first_user=request.user, second_user=second_user)
    return redirect('Chat:room', room.room_id)

@login_required(login_url='User:login')
def room(request, room_name):
    if not request.user.is_authenticated:
        return redirect('User:login')        
    user_list = request.user.friends.all()
    room = Room.objects.get(room_id=room_name)
    message_list = Message.objects.filter(room=room)    
    for message in message_list:
        message.is_seen = True
        message.save()
    rooms = Room.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
    room_message_list = []
    room_message_owners = []
    for item in rooms:
        room_message_list = Message.objects.filter(room=room, is_seen=False).exclude(user=request.user)
        for room_message in room_message_list:
            if room_message.user in room_message_owners:
                pass
            else:
                room_message_owners.append(room_message.user)
    return render(request, 'chat/chat_room.html', {
        'room_name': room_name, 'room': room, 'user_list': user_list, 'message_list': message_list, 'room_message_owners': room_message_owners
    })

@login_required(login_url='User:login')
def delete_message(request, id):
    message = Message.objects.get(user=request.user, id=id)
    if message.user == request.user:
        room_name = message.room.room_id
        message.delete()
        return redirect('Chat:room', room_name)
    else:
        return HttpResponseForbidden()