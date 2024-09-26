# File: apps/bots/models.py

from django.db import models
from django.contrib.auth.models import User

class Bot(models.Model):
    BOT_CHOICES = [
        ('telegram', 'Telegram'),
        ('whatsapp', 'WhatsApp'),
    ]
    user = models.ForeignKey(User, on_delete=models.CASCADE)  # Bot akan terkait dengan pengguna
    bot_type = models.CharField(max_length=20, choices=BOT_CHOICES)  # Jenis bot: Telegram atau WhatsApp
    
    token_telegram = models.CharField(max_length=255, unique=True, help_text="Masukkan token bot yang unik.")  # Token Telegram
    webhook_url = models.URLField(max_length=255, blank=True, help_text="URL webhook bot akan diatur secara otomatis.")  # URL webhook
    
    is_active = models.BooleanField(default=True, help_text="Status bot aktif atau tidak.")  # Status aktif atau tidaknya bot

    # Pesan otomatis
    start_message = models.TextField(blank=True, default="Selamat datang di bot!", help_text="Pesan yang dikirim saat pengguna mengetik /start.")
    help_message = models.TextField(blank=True, default="Berikut cara menggunakan bot.", help_text="Pesan yang dikirim saat pengguna mengetik /help.")
    
    messages = models.JSONField(default=list, blank=True, help_text="Daftar pesan yang diterima dan responsnya dalam format JSON.")  # Format JSON
    
    # Timestamp
    created_at = models.DateTimeField(auto_now_add=True)  # Tanggal bot dibuat
    updated_at = models.DateTimeField(auto_now=True)  # Tanggal terakhir bot diperbarui

    name = models.CharField(max_length=255, blank=True, default="Bot Saya", help_text="Nama bot.")  # Nama bot
    description = models.TextField(blank=True, default="Ini bot pertama saya", help_text="Deskripsi bot.")  # Deskripsi bot

    def __str__(self):
        return f'{self.bot_type.capitalize()} Bot - {self.user.username}'

    class Meta:
        verbose_name = "Bot"
        verbose_name_plural = "Bots"

class BotCommand(models.Model):
    bot = models.ForeignKey(Bot, related_name='commands', on_delete=models.CASCADE)
    command = models.CharField(max_length=255, help_text="Masukkan perintah seperti '/start', 'hello', dll.")
    response = models.TextField(help_text="Masukkan respons yang akan dikirim saat perintah diterima.")

    def __str__(self):
        return f"Command: {self.command} -> Response: {self.response}"

    class Meta:
        unique_together = ['bot', 'command']  # Pastikan setiap bot hanya memiliki satu perintah dengan nama yang sama.
        verbose_name = "Bot Command"
        verbose_name_plural = "Bot Commands"
