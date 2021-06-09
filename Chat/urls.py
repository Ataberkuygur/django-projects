from django.urls import path
from . import views

app_name = 'Chat'

urlpatterns = [
    path('', views.index, name='index'),
    path('start_chat/<str:second_user>', views.start_chat, name='start_chat'),
    path('<str:room_name>/', views.room, name='room'),
    path('message/delete/<int:id>/', views.delete_message, name='delete_message'),
]