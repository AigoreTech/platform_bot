# File: apps/bots/services/telegram.py
from apps.bots.models import Bot, BotCommand
import requests

def handle_update(update):
    chat_id = update['message']['chat']['id']
    text = update['message']['text'].lower()  # Mengubah ke lowercase untuk konsistensi perbandingan

    bot = Bot.objects.filter(bot_type='telegram').first()  # Misalkan kita ambil bot pertama, bisa disesuaikan

    if bot:
        # Cek apakah perintah cocok dengan yang ada di model BotCommand
        command = BotCommand.objects.filter(bot=bot, command__iexact=text).first()
        
        if command:
            response_text = command.response
        else:
            # Jika perintah tidak ditemukan, gunakan perintah default /start dan /help
            if text == "/start":
                response_text = bot.start_message
            elif text == "/help":
                response_text = bot.help_message
            else:
                response_text = 'Perintah tidak dikenal. Ketik /help untuk melihat daftar perintah.'

        send_message(bot.token, "sendMessage", {
            'chat_id': chat_id,
            'text': response_text
        })

def send_message(token, method, data):
    telegram_api_url = f'https://api.telegram.org/bot{token}/{method}'
    response = requests.post(telegram_api_url, data=data)
    if response.status_code != 200:
        logger.error(f"Failed to send message: {response.text}")  # Log error jika gagal
    return response
