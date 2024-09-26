# File: apps/bots/forms.py

from django import forms
from django.core.exceptions import ValidationError
import re  # Untuk memvalidasi pola token
from .models import Bot, BotCommand  # Mengimpor model Bot dan BotCommand

class BotForm(forms.ModelForm):
    class Meta:
        model = Bot  # Menghubungkan form dengan model Bot
        fields = ['bot_type', 'token_telegram', 'name', 'description', 'is_active', 'start_message', 'help_message']  # Tambahkan start_message dan help_message
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Masukkan nama bot'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Deskripsi bot'}),
            'start_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pesan yang dikirim saat /start'}),
            'help_message': forms.Textarea(attrs={'class': 'form-control', 'rows': 3, 'placeholder': 'Pesan yang dikirim saat /help'}),
        }
        help_texts = {
            'token_telegram': 'Masukkan token unik yang diterima dari platform Telegram.',
            'name': 'Nama bot dapat diubah sesuai keinginan.',
            'description': 'Deskripsi singkat tentang bot dan fungsinya.',
            'start_message': 'Pesan yang dikirim ketika pengguna mengetik /start.',
            'help_message': 'Pesan yang dikirim ketika pengguna mengetik /help.',
        }

    # Validasi khusus untuk token Telegram
    def clean_token_telegram(self):
        token_telegram = self.cleaned_data.get('token_telegram')
        bot_type = self.cleaned_data.get('bot_type')

        # Validasi hanya jika bot_type adalah Telegram
        if bot_type == 'telegram':
            # Pola token Telegram: angka-angka diikuti dengan titik dua, lalu serangkaian karakter acak
            if token_telegram and not re.match(r'^\d+:[\w-]+$', token_telegram):
                raise ValidationError("Token Telegram tidak valid. Pastikan format token adalah seperti '123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11'.")

        return token_telegram

    # Validasi nama bot
    def clean_name(self):
        name = self.cleaned_data.get('name')
        if not name.strip():
            raise ValidationError("Nama bot tidak boleh kosong.")
        return name

    # Validasi deskripsi bot
    def clean_description(self):
        description = self.cleaned_data.get('description')
        if len(description) > 500:
            raise ValidationError("Deskripsi bot tidak boleh lebih dari 500 karakter.")
        return description

class BotCommandForm(forms.ModelForm):
    class Meta:
        model = BotCommand
        fields = ['command', 'response']  # Field yang akan ditampilkan dalam form
        widgets = {
            'command': forms.TextInput(attrs={'placeholder': 'Contoh: /start, /help'}),
            'response': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Masukkan respon yang akan dikirim.'}),
        }
        help_texts = {
            'command': 'Masukkan perintah seperti "/start", "/help", atau lainnya.',
            'response': 'Masukkan respons yang akan dikirim saat perintah diterima.',
        }
