# Generated by Django 5.0.6 on 2024-09-25 04:41

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Bot',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('bot_type', models.CharField(choices=[('telegram', 'Telegram'), ('whatsapp', 'WhatsApp')], max_length=20)),
                ('token_telegram', models.CharField(help_text='Masukkan token bot yang unik.', max_length=255, unique=True)),
                ('webhook_url', models.URLField(blank=True, help_text='URL webhook bot akan diatur secara otomatis.', max_length=255)),
                ('is_active', models.BooleanField(default=True, help_text='Status bot aktif atau tidak.')),
                ('start_message', models.TextField(blank=True, default='Selamat datang di bot!', help_text='Pesan yang dikirim saat pengguna mengetik /start.')),
                ('help_message', models.TextField(blank=True, default='Berikut cara menggunakan bot.', help_text='Pesan yang dikirim saat pengguna mengetik /help.')),
                ('messages', models.JSONField(blank=True, default=list, help_text='Daftar pesan yang diterima dan responsnya dalam format JSON.')),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('name', models.CharField(blank=True, default='Bot Saya', help_text='Nama bot.', max_length=255)),
                ('description', models.TextField(blank=True, default='Ini bot pertama saya', help_text='Deskripsi bot.')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Bot',
                'verbose_name_plural': 'Bots',
            },
        ),
    ]
