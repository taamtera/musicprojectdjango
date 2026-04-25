from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from backend.models import Song

class SongListView(LoginRequiredMixin, ListView):
    model = Song
    template_name = 'frontend/song_list.html'

    def get_queryset(self):
        queryset = super().get_queryset()
        sort_by = self.request.GET.get('sort', '-created_at')
        genre_filter = self.request.GET.get('genre', '')
        
        if genre_filter:
            queryset = queryset.filter(genre__icontains=genre_filter)
            
        if sort_by in ['title', '-title', 'created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
            
        return queryset

import requests
import time
from django.conf import settings

class SongCreateView(LoginRequiredMixin, CreateView):
    model = Song
    fields = ['title', 'genre', 'tags', 'description', 'generation_method']
    template_name = 'generic_form.html'
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
            
        return super().form_valid(form)

    def _call_mock_api(self, song):
        """Simulate an API call with a mock response."""
        song.gen_status = 'in-progress'
        song.audio_url = "https://www.soundhelix.com/examples/mp3/SoundHelix-Song-4.mp3"
        # In a real app, you might use a task queue like Celery for this

    def _call_suno_api(self, song):
        """Call the real Suno API."""
        url = "https://api.sunoapi.org/api/v1/generate"
        token = settings.SUNO_API_TOKEN
        
        payload = {
            "customMode": True,
            "instrumental": False,
            "model": "V4_5ALL",
            "prompt": song.description or "A music track",
            "style": song.genre,
            "title": song.title,
            "negativeTags": "",
        }
        
        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        try:
            response = requests.post(url, json=payload, headers=headers, timeout=10)
            data = response.json()
            
            if response.status_code == 200 and data.get("code") == 200:
                # The API returns a taskId. For now, we'll store it in description or similar
                # or just mark it as in-progress.
                song.gen_status = 'in-progress'
                # Note: Real Suno API uses a callback or polling to get the actual URL
            else:
                song.gen_status = 'failed'
        except Exception as e:
            song.gen_status = 'failed'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Song'
        return context

class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Song
    fields = ['title', 'genre', 'tags', 'description', 'gen_status', 'audio_url']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('song-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Song'
        return context

class SongDeleteView(LoginRequiredMixin, DeleteView):
    model = Song
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('song-list')
