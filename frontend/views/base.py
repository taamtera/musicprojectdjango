from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.http import FileResponse, HttpResponse
from django.conf import settings
import os
from pathlib import Path

def index(request):
    return render(request, 'pages/index.html')

def popup_callback(request):
    return render(request, 'pages/popup_callback.html')

def dev_login(request):
    """Automatically log in as the test user for development."""
    if not settings.DEBUG:
        messages.error(request, "Developer bypass is only available in debug mode.")
        return redirect('song-list')

    User = get_user_model()
    candidates = User.objects.filter(username='testuser')
    user = candidates.first()

    if user is None:
        user = User.objects.create(
            username='testuser',
            email='test@example.com',
            name='Test User',
            is_staff=True,
        )
        user.set_unusable_password()
        user.save(update_fields=['password'])
        messages.info(request, "Created missing test user automatically.")
    elif candidates.count() > 1:
        messages.warning(request, "Multiple test users found. Signed in with the first match.")

    login(request, user, backend='django.contrib.auth.backends.ModelBackend')
    messages.success(request, f"Bypass successful! Logged in as {user.username}")
    
    return redirect('song-list')

def serve_audio(request, filename):
    """Serve audio files with range request support for seeking."""
    file_path = os.path.join(settings.MEDIA_ROOT, 'songs', filename)
    
    # Security check - ensure the file is within MEDIA_ROOT
    try:
        file_path_obj = Path(file_path).resolve()
        media_root_obj = Path(settings.MEDIA_ROOT).resolve()
        file_path_obj.relative_to(media_root_obj)
    except (ValueError, AttributeError):
        return HttpResponse(status=403)
    
    if not os.path.exists(file_path):
        return HttpResponse(status=404)
    
    file_size = os.path.getsize(file_path)
    
    # Handle range requests for seeking
    range_header = request.META.get('HTTP_RANGE', '')
    if range_header.startswith('bytes='):
        try:
            range_value = range_header.replace('bytes=', '')
            start, end = range_value.split('-')
            start = int(start) if start else 0
            end = int(end) if end else file_size - 1
            
            if start >= file_size or end >= file_size:
                return HttpResponse(status=416)
            
            file_obj = open(file_path, 'rb')
            file_obj.seek(start)
            response = FileResponse(file_obj, status=206)
            response['Content-Range'] = f'bytes {start}-{end}/{file_size}'
            response['Content-Length'] = str(end - start + 1)
            response['Content-Type'] = 'audio/mpeg'
            response['Accept-Ranges'] = 'bytes'
            return response
        except (ValueError, IndexError):
            pass
    
    # Normal response without range
    response = FileResponse(open(file_path, 'rb'), content_type='audio/mpeg')
    response['Content-Length'] = file_size
    response['Accept-Ranges'] = 'bytes'
    return response
