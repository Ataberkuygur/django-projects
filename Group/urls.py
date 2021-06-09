from django.urls import path
from .views import GroupDetail

app_name = 'Group'

urlpatterns = [
    path('create/', GroupDetail, name='detail'),
    path('detail/<slug>/', GroupDetail, name='detail'),
]
