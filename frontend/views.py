from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from backend.models import User, Song, ShareLink
from django.shortcuts import render
from django.contrib.auth.decorators import login_required

# Index view
def index(request):
    return render(request, 'index.html')

def popup_callback(request):
    return render(request, 'frontend/popup_callback.html')

# User Views
class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'frontend/user_list.html'

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['username', 'email', 'name', 'is_staff']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create User'
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'name', 'is_staff']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('user-list')

# Song Views
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

class SongCreateView(LoginRequiredMixin, CreateView):
    model = Song
    fields = ['title', 'genre', 'tags', 'description', 'gen_status', 'generated_by', 'audio_url']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('song-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Song'
        return context

class SongUpdateView(LoginRequiredMixin, UpdateView):
    model = Song
    fields = ['title', 'genre', 'tags', 'description', 'gen_status', 'generated_by', 'audio_url']
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

# ShareLink Views
class ShareLinkListView(LoginRequiredMixin, ListView):
    model = ShareLink
    template_name = 'frontend/sharelink_list.html'

class ShareLinkCreateView(LoginRequiredMixin, CreateView):
    model = ShareLink
    fields = ['song', 'creator', 'email', 'can_view', 'can_download', 'can_share_forward']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('sharelink-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Share Link'
        return context

class ShareLinkUpdateView(LoginRequiredMixin, UpdateView):
    model = ShareLink
    fields = ['song', 'creator', 'email', 'can_view', 'can_download', 'can_share_forward']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('sharelink-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Share Link'
        return context

class ShareLinkDeleteView(LoginRequiredMixin, DeleteView):
    model = ShareLink
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('sharelink-list')
