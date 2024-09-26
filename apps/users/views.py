# File: apps/users/views.py

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from apps.users.forms import EditProfileForm
from apps.dashboard.models import ActivityLog
from django.utils import timezone

@login_required
def profile(request):
    user = request.user
    profile = user.userprofile  # Dapatkan profil user yang sedang login
    
    if request.method == 'POST':
        form = EditProfileForm(request.POST, request.FILES, instance=profile, user=user)
        if form.is_valid():
            form.save()

            # Membuat log aktivitas ketika profil diperbarui
            ActivityLog.objects.create(
                user=user, 
                action="Mengedit profil", 
                timestamp=timezone.now()
            )

            return redirect('profile')  # Redirect ke halaman profil setelah berhasil
    else:
        form = EditProfileForm(instance=profile, user=user)
    
    # Definisikan context yang akan diberikan ke template
    context = {
        'ASSETS_ROOT': '/static/assets',  # Aset statis
        'form': form,  # Form untuk mengedit profil
        'profile': profile,  # Profil user yang sedang login
    }

    return render(request, 'users/profile.html', context)
