# File: apps/webhook/urls.py

from django.urls import path
from .views import telegram_webhook, whatsapp_webhook

urlpatterns = [
    # Endpoint webhook untuk Telegram
    path('telegram/', telegram_webhook, name='telegram_webhook'),
    # Endpoint webhook untuk WhatsApp
    path('whatsapp/', whatsapp_webhook, name='whatsapp_webhook'),
]
