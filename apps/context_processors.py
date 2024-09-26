# File: apps/context_processors.py

from django.conf import settings

def cfg_assets_root(request):
    # Mengambil nilai ASSETS_ROOT dari settings.py dan mengirimkannya ke template
    return {'ASSETS_ROOT': settings.ASSETS_ROOT}
