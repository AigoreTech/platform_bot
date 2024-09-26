# File: apps/webhook/views.py

import json
import requests
from django.http import HttpResponse, HttpResponseBadRequest
from django.views.decorators.csrf import csrf_exempt
import logging
from apps.bots.services.telegram import handle_update as handle_telegram_update
from apps.bots.services.whatsapp import handle_update as handle_whatsapp_update

logger = logging.getLogger(__name__)

@csrf_exempt
def telegram_webhook(request):
    if request.method == 'POST':
        try:
            update = json.loads(request.body.decode('utf-8'))
            logger.info(f"Telegram update received: {update}")

            if 'message' in update:
                handle_telegram_update(update)
                return HttpResponse('ok')  # Pastikan mengembalikan respons yang valid

            return HttpResponseBadRequest('No message found in update')
        except json.JSONDecodeError:
            logger.error("Invalid JSON received.")
            return HttpResponseBadRequest('Invalid JSON format')
        except Exception as e:
            logger.error(f"Error processing Telegram webhook: {e}")
            return HttpResponse('Error', status=500)
    return HttpResponseBadRequest('Bad Request', status=400)


@csrf_exempt
def whatsapp_webhook(request):
    if request.method == 'POST':
        try:
            # Jika payload adalah form-urlencoded, ambil dari request.POST
            if 'From' in request.POST and 'Body' in request.POST:
                update = {
                    'From': request.POST['From'],
                    'Body': request.POST['Body']
                }
                return handle_whatsapp_update(update)

            return HttpResponse('ok')

        except Exception as e:
            logger.error(f"Error processing webhook: {e}")
            return HttpResponseBadRequest('Failed to process update')
    else:
        return HttpResponseBadRequest('Bad Request')


def set_telegram_webhook(token_telegram, url):
    TELEGRAM_API_URL = f'https://api.telegram.org/bot{token_telegram}/'
    response = requests.post(TELEGRAM_API_URL + "setWebhook?url=" + url).json()

    if not response.get('ok'):
        logger.error(f"Failed to set Telegram webhook: {response}")
    else:
        logger.info(f"Telegram webhook set successfully: {response}")

    return response

def set_whatsapp_webhook(url):
    logger.info(f"Webhook WhatsApp harus diatur melalui dashboard Twilio ke URL: {url}")
    return {"status": "Webhook configuration needed via Twilio dashboard."}
