from django.urls import path
from .views import AddictionDetail, AddictionIndex

app_name='Addiction'

urlpatterns = [
    path('index/', AddictionIndex, name='index'),
    path('detail/<slug>/', AddictionDetail, name='detail'),
]
