# File: apps/bots/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_bot, name='create_bot'),  # URL untuk halaman pembuatan bot
    path('manage/', views.manage_bots, name='manage_bots'),  # URL untuk halaman manajemen bot
    path('edit_bot/<int:bot_id>/', views.edit_bot, name='edit_bot'),  # Menggunakan bot_id sebagai parameter
    path('add_command/<int:bot_id>/', views.add_command, name='add_command'), # URL untuk menambah command
    path('edit_command/<int:command_id>/', views.edit_command, name='edit_command'),  # URL untuk edit command
]
