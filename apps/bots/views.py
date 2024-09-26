# File: apps/bots/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import BotForm,BotCommandForm
from .models import Bot,BotCommand
from django.conf import settings
from apps.webhook.views import set_telegram_webhook
from apps.webhook.views import set_whatsapp_webhook
from apps.dashboard.models import ActivityLog

WEBHOOK_URL = settings.WEBHOOK_URL

@login_required
def create_bot(request):
    if request.method == 'POST':
        form = BotForm(request.POST)
        if form.is_valid():
            bot = form.save(commit=False)
            bot.user = request.user
            bot.is_active = True  # Set bot aktif secara default

            # Tentukan webhook URL sesuai dengan platform
            if bot.bot_type == 'telegram':
                bot.webhook_url = f'{WEBHOOK_URL}/telegram/'
            elif bot.bot_type == 'whatsapp':
                bot.webhook_url = f'{WEBHOOK_URL}/whatsapp/'

            bot.save()

            # Set webhook berdasarkan tipe bot
            if bot.bot_type == 'telegram':
                set_telegram_webhook(bot.token_telegram, bot.webhook_url)
                # Tambahkan pesan sukses untuk bot Telegram
                messages.success(request, 'Bot Telegram berhasil dibuat!')
            elif bot.bot_type == 'whatsapp':
                set_whatsapp_webhook(bot.webhook_url)
                # Tambahkan pesan sukses untuk bot WhatsApp
                messages.success(request, f'Bot WhatsApp berhasil dibuat. Silakan atur URL webhook berikut di dashboard Twilio: {bot.webhook_url}')

            # Tambahkan log aktivitas
            ActivityLog.objects.create(
                user=request.user,
                action=f"Membuat bot baru: {bot.name}"
            )

            return redirect('manage_bots')
    else:
        form = BotForm()

    return render(request, 'bots/create_bot.html', {'form': form})

@login_required  # Pastikan hanya pengguna yang login yang bisa mengakses view ini
def manage_bots(request):
    bots = Bot.objects.filter(user=request.user)  # Ambil daftar bot milik pengguna yang sedang login

    if request.method == 'POST':
        if 'delete' in request.POST:  # Cek apakah ada permintaan untuk menghapus bot
            bot_id = request.POST.get('delete')  # Ambil ID bot yang ingin dihapus dari form
            bot = get_object_or_404(Bot, id=bot_id, user=request.user)  # Pastikan bot milik pengguna yang sedang login

            # Menyimpan aktivitas penghapusan ke dalam log sebelum bot dihapus
            ActivityLog.objects.create(
                user=request.user,
                action=f"Bot {bot.name} telah dihapus"
            )
            bot.delete()  # Hapus bot dari database
            messages.success(request, 'Bot berhasil dihapus.')  # Tambahkan pesan setelah bot dihapus
            return redirect('manage_bots')  # Setelah bot dihapus, kembali ke halaman manajemen bot

        elif 'delete_command' in request.POST:
            command_id = request.POST.get('delete_command')  # Mendapatkan ID command yang akan dihapus
            command = get_object_or_404(BotCommand, id=command_id)  # Mendapatkan command berdasarkan ID

            # Pastikan command milik bot milik pengguna
            if command.bot.user == request.user:
                # Menyimpan aktivitas penghapusan command ke dalam log
                ActivityLog.objects.create(
                    user=request.user,
                    action=f"Menghapus command: {command.command} dari bot {command.bot.name}"
                )
                command.delete()  # Menghapus command dari database
                messages.success(request, 'Command berhasil dihapus.')  # Tambahkan pesan setelah command dihapus
            else:
                messages.error(request, 'Akses ditolak. Command ini bukan milik Anda.')
            
            return redirect('manage_bots')  # Mengarahkan kembali ke halaman manage bots

    return render(request, 'bots/manage_bots.html', {'bots': bots})  # Render halaman dengan daftar bot yang dimiliki pengguna

@login_required
def edit_bot(request, bot_id):
    bot = get_object_or_404(Bot, id=bot_id)  # Ambil bot berdasarkan ID
    if request.method == 'POST':
        form = BotForm(request.POST, instance=bot)  # Muat data ke form
        if form.is_valid():
            form.save()  # Simpan data yang telah diedit

            # Tambahkan log aktivitas setelah bot berhasil diedit
            ActivityLog.objects.create(
                user=request.user,
                action=f"Bot {bot.name} telah diperbarui",
                bot=bot
            )

            return redirect('manage_bots')  # Alihkan ke halaman pengelolaan bot
    else:
        form = BotForm(instance=bot)  # Jika bukan POST, buat form dengan data bot

    context = {
        'form': form,
        'bot': bot,
    }
    return render(request, 'bots/edit_bot.html', context)  # Tampilkan template dengan context

@login_required
def add_command(request, bot_id):
    bot = get_object_or_404(Bot, id=bot_id, user=request.user)  # Mendapatkan bot berdasarkan ID dan memastikan user adalah pemilik bot

    if request.method == 'POST':
        form = BotCommandForm(request.POST)  # Membuat form berdasarkan data POST
        if form.is_valid():
            command = form.save(commit=False)  # Simpan command baru tapi belum ke database
            command.bot = bot  # Menetapkan bot terkait dengan command
            command.save()  # Menyimpan command ke database

            # Mencatat aktivitas penambahan command ke dalam log
            ActivityLog.objects.create(
                user=request.user,
                action=f"Menambahkan command baru: {command.command} untuk bot {bot.name}"
            )

            return redirect('manage_bots')  # Setelah berhasil menyimpan, redirect ke halaman edit bot
    else:
        form = BotCommandForm()  # Jika GET, tampilkan form kosong

    return render(request, 'bots/add_command.html', {'form': form, 'bot': bot})  # Render template dengan form

@login_required
def edit_command(request, command_id):
    command = get_object_or_404(BotCommand, id=command_id)  # Ambil command berdasarkan ID
    bot = command.bot  # Mendapatkan bot terkait dengan command

    if request.method == 'POST':
        form = BotCommandForm(request.POST, instance=command)  # Muat data POST ke dalam form
        if form.is_valid():
            form.save()  # Simpan perubahan command ke dalam database

            # Catat aktivitas pengeditan command ke dalam log
            ActivityLog.objects.create(
                user=request.user,
                action=f"Mengedit command: {command.command} di bot {bot.name}"
            )

            return redirect('manage_bots')  # Setelah berhasil menyimpan, alihkan kembali ke halaman edit bot
    else:
        form = BotCommandForm(instance=command)  # Jika bukan POST, tampilkan form dengan data command yang ada

    return render(request, 'bots/edit_command.html', {'form': form, 'bot': bot})  # Render template dengan form dan bot terkait
