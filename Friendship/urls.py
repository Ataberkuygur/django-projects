from django.urls import path
from .views import send_request, accept_request

app_name = 'Friendship'

urlpatterns = [
    path("send_request/<slug>/", send_request, name="send_request"),
    path("accept_request/<slug>/", accept_request, name="accept_request"),
]
