from .views import CustomUserLogin, RegisterCustomUser, CustomUserProfile, UpdateCustomUser
from django.contrib.auth.views import LogoutView
from django.urls import path

app_name = 'User'

urlpatterns = [
    path('register/', RegisterCustomUser, name = 'register'),
    path('update/<slug>/', UpdateCustomUser, name = 'update'),
    path('profile/<slug>/', CustomUserProfile, name = 'profile'),
    path('login/', CustomUserLogin, name = 'login'),
    path('logout/', LogoutView.as_view(template_name='registration/logout.html'), name = 'logout'),
]
