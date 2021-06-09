"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls.static import static
from django.conf import settings
from .views import Explore, Notifications, Settings, CategoryCreate, CategoryDelete, CategoryListDelete, GoalCreate

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('User.urls')),
    path('friendship/', include('Friendship.urls')),
    path('group/', include('Group.urls')),
    path('chat/', include('Chat.urls')),
    path('', include('Task.urls')),
    path('pomodoro/', include('Pomodoro.urls')),
    path('addiction/', include('Addiction.urls')),
    path('explore/', Explore, name = 'explore'),
    path('settings/<slug>/', Settings, name = 'settings'),
    path('notifications/<slug>/', Notifications, name = 'notifications'),
    path('category/create/', CategoryCreate, name = 'category_create'),
    path('category/delete/', CategoryDelete, name = 'category_delete'),
    path('category/list/delete/', CategoryListDelete, name = 'category_list_delete'),
    path('goal/create/', GoalCreate, name = 'goal_create'),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
