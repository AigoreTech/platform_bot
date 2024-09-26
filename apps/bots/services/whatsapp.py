# File: apps/bots/services/whatsapp.py

from django.http import HttpResponse  # Untuk mengembalikan respon HTTP
from django.views.decorators.csrf import csrf_exempt  # Agar view dapat diakses tanpa validasi CSRF
from twilio.twiml.messaging_response import MessagingResponse  # Untuk membuat balasan ke Twilio API
from apps.bots.models import Bot, BotCommand  # Mengimpor model Bot dan BotCommand dari aplikasi bots
import logging  # Untuk logging aktivitas dan error

logger = logging.getLogger(__name__)  # Inisialisasi logger

@csrf_exempt  # Dekorator untuk menonaktifkan validasi CSRF pada view ini
def handle_update(update):
    # Mendapatkan pengirim pesan dan isi pesan
    user = update['From']  
    message = update['Body'].strip().lower()  # Mengubah pesan ke lowercase untuk perbandingan

    # Logging pesan yang diterima
    logger.info(f'{user} says {message}')

    # Mengambil bot pertama yang bertipe WhatsApp dari database
    bot = Bot.objects.filter(bot_type='whatsapp').first()
    response = MessagingResponse()  # Membuat respon menggunakan Twilio's MessagingResponse

    if bot:  # Jika bot ditemukan
        # Cek apakah perintah cocok dengan yang ada di model BotCommand
        command = BotCommand.objects.filter(bot=bot, command__iexact=message).first()
        
        if command:
            response_text = command.response  # Dapatkan respons dari perintah
        else:
            # Jika perintah tidak ditemukan, gunakan perintah default /start dan /help
            if message == "/start":
                response_text = bot.start_message  # Pesan sambutan
            elif message == "/help":
                response_text = bot.help_message  # Pesan bantuan
            else:
                response_text = 'Perintah tidak dikenal. Ketik /help untuk melihat daftar perintah.'  # Pesan default

        response.message(response_text)  # Mengirim balasan pesan
    else:
        response.message('Bot tidak ditemukan.')  # Jika bot tidak ditemukan di database

    # Mengembalikan respon sebagai HTTP response
    return HttpResponse(str(response))

