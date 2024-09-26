# File: apps/authentication/views.py

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login,logout
from django.contrib import messages
from .forms import UserRegistrationForm,UserLoginForm
from .models import UserProfile

# View untuk halaman home
def home(request):
    context = {
        'ASSETS_ROOT': '/static/assets',  # Tambahan path untuk asset static jika diperlukan
        }
    return render(request, 'home/home.html', context)


# View untuk menangani registrasi pengguna baru
def user_register(request):
    if request.method == 'POST':
        # Memeriksa apakah request adalah POST dan memproses data form
        form = UserRegistrationForm(request.POST, request.FILES)
        if form.is_valid():
            # Menyimpan data pengguna ke dalam model User
            user = form.save()
            # Membuat dan menyimpan profil pengguna yang terhubung ke User
            UserProfile.objects.create(
                user=user,
                city=form.cleaned_data.get('city', ''),
                address=form.cleaned_data.get('address', ''),
                country=form.cleaned_data.get('country', ''),
                postal_code=form.cleaned_data.get('postal_code', ''),
                about=form.cleaned_data.get('about', ''),
                foto_profile=request.FILES.get('foto_profile', None)
            )
            # Log in pengguna secara otomatis setelah registrasi
            login(request, user)
            # Redirect ke halaman home atau dashboard setelah registrasi berhasil
            return redirect('dashboard')
    else:
        # Jika request bukan POST, buat form kosong untuk ditampilkan di halaman
        form = UserRegistrationForm()

    # Menyiapkan konteks untuk template
    context = {
        'form': form,
        'ASSETS_ROOT': '/static/assets',  # Menyertakan path assets
    }

    # Render halaman register dengan form yang sudah disiapkan
    return render(request, 'account/register.html', context)


# View untuk login pengguna
def user_login(request):
    if request.method == 'POST':
        # Mengambil data dari form dan memvalidasi
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            # Autentikasi pengguna
            user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
            if user is not None:
                # Login pengguna jika data valid
                login(request, user)
                messages.success(request, 'Login berhasil.')
                return redirect('dashboard')  # Mengarahkan pengguna setelah login berhasil
            else:
                # Menampilkan pesan error jika autentikasi gagal
                messages.error(request, 'Invalid username or password.')
    else:
        form = UserLoginForm()

    context = {
        'ASSETS_ROOT': '/static/assets',  # Tambahan path untuk asset static jika diperlukan
        'form': form,
    }
    return render(request, 'account/login.html', context)

# View untuk logout pengguna
def user_logout(request):
    # Logout pengguna
    logout(request)
    
    # Hapus cookies kustom (misalnya, 'remember_me')
    if 'remember_me' in request.COOKIES:
        response = redirect('login')
        response.delete_cookie('remember_me')
        return response
    
    # Setelah logout, arahkan pengguna kembali ke halaman login
    return redirect('login')
