from django.contrib.auth.decorators import login_required
from django.db.models import Q
from Chat.models import Message, Room
from User.models import CustomUser
from Friendship.models import Friendship

def notification_data(request):
    if request.user.is_authenticated:
        context = dict()
        #Arkadaşlık istekleri ve sayısı
        requests = Friendship.objects.filter(receiver=request.user, status='send')
        context['requests'] = requests

        #Odalardan gelen okunmamış mesajlar ve sayısı
        rooms = Room.objects.filter(Q(first_user=request.user) | Q(second_user=request.user))
        room_message_list = []
        not_seen_message_users = []
        for room in rooms:
            room_message_list = Message.objects.filter(room=room, is_seen=False).exclude(user=request.user)
            for room_message in room_message_list:
                if room_message.user in not_seen_message_users:
                    pass
                else:
                    not_seen_message_users.append(room_message.user)
        notification_count = len(not_seen_message_users) + len(requests)
        context['not_seen_message_users'] = not_seen_message_users
        if notification_count > 0:
            context['notification_count'] = notification_count
        return context
    else:
        context = {}
        return context
        
