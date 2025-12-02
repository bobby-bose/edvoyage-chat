from django.urls import path
from . import views

urlpatterns = [
    path('conversations', views.conversations_get),
    path('messages', views.messages_get),
    path('send', views.send_message),
    path('users', views.users_list),
]
