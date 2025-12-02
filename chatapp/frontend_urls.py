from django.urls import path
from . import views

urlpatterns = [
    path('', views.index_page, name='index_page'),  # Root path
    path('home/', views.index_page, name='index_page_alt'),  # Alternative
    path('chat/', views.chat_page, name='chat_page'),
]
