from django.shortcuts import render, redirect
from django.contrib.auth import login
from backend.models import User
from django.contrib import messages

def index(request):
    return render(request, 'pages/index.html')

def popup_callback(request):
    return render(request, 'pages/popup_callback.html')

def dev_login(request):
    """Automatically log in as the test user for development."""
    try:
        user = User.objects.get(username='testuser')
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        messages.success(request, f"Bypass successful! Logged in as {user.username}")
    except User.DoesNotExist:
        messages.error(request, "Test user not found. Please run migrations.")
    
    return redirect('index')
