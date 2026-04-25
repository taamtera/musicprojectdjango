from django.urls import reverse_lazy, reverse
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.views import View
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from backend.models import Song
from .mixins import LandingLoginRequiredMixin
import json
import requests
import time
from django.conf import settings
from django.template.loader import render_to_string
from django.http import JsonResponse

class SongListView(LandingLoginRequiredMixin, ListView):
    model = Song
    template_name = 'songs/list.html'
    context_object_name = 'songs'

    def get_queryset(self):
        queryset = self.request.user.listens_to.all()

        from django.db.models import Q
        sort_by = self.request.GET.get('sort', '-created_at')
        query = self.request.GET.get('title', '').strip()

        if query:
            queryset = queryset.filter(
                Q(title__icontains=query) |
                Q(genre__icontains=query) |
                Q(description__icontains=query)
            )

        sort_options = {
            '-created_at': '-created_at',   # Newest
            'created_at': 'created_at',     # Oldest
            'title': 'title',               # Title A-Z
            '-title': '-title',             # Title Z-A
            'genre': 'genre',               # Genre A-Z
            '-genre': '-genre',             # Genre Z-A
            'status_done': '-gen_status',   # Status Done First
            'status_progress': 'gen_status' # Status In Progress First
        }

        queryset = queryset.order_by(sort_options.get(sort_by, '-created_at'))

        return queryset

    def render_to_response(self, context, **response_kwargs):
        # 👇 THIS is what enables no-refresh search
        if self.request.headers.get('x-requested-with') == 'XMLHttpRequest':
            html = render_to_string(
                'songs/partials/song_list.html',
                context,
                request=self.request
            )
            return JsonResponse({'html': html})

        return super().render_to_response(context, **response_kwargs)

@method_decorator(csrf_exempt, name='dispatch')
class SongCallbackView(View):
    def post(self, request, token, *args, **kwargs):
        try:
            song = Song.objects.get(callback_token=token)
            data = json.loads(request.body)
            
            # Example: Suno callback might contain 'data' list with objects having 'audio_url'
            # Adjust this logic based on the actual API response structure
            if isinstance(data, dict):
                audio_url = data.get('audio_url') or data.get('url')
                if not audio_url and 'data' in data and isinstance(data['data'], list):
                    audio_url = data['data'][0].get('audio_url')
                
                if audio_url:
                    song.audio_url = audio_url
                    song.gen_status = 'done'
                    song.save()
                    return JsonResponse({'status': 'success'})
            
            return JsonResponse({'status': 'error', 'message': 'No audio URL found'}, status=400)
            
        except Song.DoesNotExist:
            return JsonResponse({'status': 'error', 'message': 'Invalid token'}, status=404)
        except Exception as e:
            return JsonResponse({'status': 'error', 'message': str(e)}, status=400)


class SongCreateView(LandingLoginRequiredMixin, CreateView):
    model = Song
    fields = ['title', 'genre', 'description', 'generation_method']
    template_name = 'common/form.html'
    success_url = reverse_lazy('song-list')

    def form_valid(self, form):
        # Automatically set the user who generated the song
        form.instance.generated_by = self.request.user
        
        # Determine which API to call
        method = form.cleaned_data.get('generation_method')
        
        if method == 'suno':
            self._call_suno_api(form.instance)
        else:
            self._call_mock_api(form.instance)
            
        response = super().form_valid(form)
        
        # Add the newly created song to the user's library (listens_to)
        self.request.user.listens_to.add(self.object)
        
        return response

    def _call_mock_api(self, song):
        """Simulate an API call with a mock response."""
        import secrets
        song.task_id = f"mock{secrets.token_hex(16)}" 
        song.gen_status = 'in-progress'
        song.audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
        # In a real app, you might use a task queue like Celery for this

    def _call_suno_api(self, song):
        """Call the real Suno API."""
        url = "https://api.sunoapi.org/api/v1/generate"
        token = settings.SUNO_API_TOKEN
        
        # Construct the absolute callback URL
        callback_url = self.request.build_absolute_uri(
            reverse('song-callback', kwargs={'token': song.callback_token})
        )
        
        # Override for local testing if needed
        if '127.0.0.1' in callback_url or 'localhost' in callback_url:
            callback_url = callback_url.replace('127.0.0.1:8000', 'taamtera.space')
            callback_url = callback_url.replace('localhost:8000', 'taamtera.space')
            # Ensure it uses https if that's what your domain uses
            if not callback_url.startswith('https'):
                callback_url = callback_url.replace('http://', 'https://')
        
        payload = {
            "customMode": True,
            "instrumental": False,
            "model": "V4_5ALL",
            "prompt": song.description or "A music track",
            "style": song.genre,
            "title": song.title,
            "negativeTags": "",
            "callbackUrl": callback_url,
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and data.get("code") == 200:
                # Extract taskId from response
                task_id = data.get("data")
                if isinstance(task_id, dict):
                    task_id = task_id.get("taskId")
                
                song.task_id = task_id
                song.gen_status = 'in-progress'
            else:
                song.gen_status = 'failed'
        except Exception as e:
            song.gen_status = 'failed'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Song'
        return context

class SongUpdateView(LandingLoginRequiredMixin, UpdateView):
    model = Song
    fields = ['title', 'genre', 'description']
    template_name = 'common/form.html'
    success_url = reverse_lazy('song-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Song'
        return context

class SongDeleteView(LandingLoginRequiredMixin, DeleteView):
    model = Song
    template_name = 'common/confirm_delete.html'
    success_url = reverse_lazy('song-list')
