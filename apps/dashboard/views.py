# File: apps/dashboard/views.py
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from apps.authentication.models import UserProfile
from apps.dashboard.models import ActivityLog

@login_required
def dashboard(request):
    # Ambil profil pengguna yang sedang login
    user_profile = UserProfile.objects.filter(user=request.user).first()
    
    # Ambil aktivitas log pengguna yang sedang login
    activity_logs = ActivityLog.objects.filter(user=request.user).order_by('-timestamp')

    # Data yang akan diteruskan ke template
    context = {
        'ASSETS_ROOT': '/static/assets',
        'user_profile': user_profile,
        'activity_logs': activity_logs,
    }

    # Merender template dashboard.html dengan data yang diambil
    return render(request, 'dashboard/dashboard.html', context)
