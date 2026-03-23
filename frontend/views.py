from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from backend.models import User, Song, Library, LibraryEntry, ShareLink
from django.shortcuts import render

# Index view
def index(request):
    return render(request, 'frontend/index.html')

# User Views
class UserListView(ListView):
    model = User
    template_name = 'frontend/user_list.html'

class UserCreateView(CreateView):
    model = User
    fields = ['username', 'email', 'name', 'is_staff']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create User'
        return context

class UserUpdateView(UpdateView):
    model = User
    fields = ['username', 'email', 'name', 'is_staff']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context

class UserDeleteView(DeleteView):
    model = User
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('user-list')

# Song Views
class SongListView(ListView):
    model = Song
    template_name = 'frontend/song_list.html'

class SongCreateView(CreateView):
    model = Song
    fields = ['title', 'genre', 'description', 'gen_status', 'generated_by']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('song-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Song'
        return context

class SongUpdateView(UpdateView):
    model = Song
    fields = ['title', 'genre', 'description', 'gen_status', 'generated_by']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('song-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Song'
        return context

class SongDeleteView(DeleteView):
    model = Song
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('song-list')

# Library Views
class LibraryListView(ListView):
    model = Library
    template_name = 'frontend/library_list.html'

class LibraryCreateView(CreateView):
    model = Library
    fields = ['user_generated', 'user_shared']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('library-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Library'
        return context

class LibraryUpdateView(UpdateView):
    model = Library
    fields = ['user_generated', 'user_shared']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('library-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Library'
        return context

class LibraryDeleteView(DeleteView):
    model = Library
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('library-list')

# LibraryEntry Views
class LibraryEntryListView(ListView):
    model = LibraryEntry
    template_name = 'frontend/libraryentry_list.html'

class LibraryEntryCreateView(CreateView):
    model = LibraryEntry
    fields = ['library', 'song', 'entry_type']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('libraryentry-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Library Entry'
        return context

class LibraryEntryUpdateView(UpdateView):
    model = LibraryEntry
    fields = ['library', 'song', 'entry_type']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('libraryentry-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Library Entry'
        return context

class LibraryEntryDeleteView(DeleteView):
    model = LibraryEntry
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('libraryentry-list')

# ShareLink Views
class ShareLinkListView(ListView):
    model = ShareLink
    template_name = 'frontend/sharelink_list.html'

class ShareLinkCreateView(CreateView):
    model = ShareLink
    fields = ['song', 'creator', 'email', 'perm']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('sharelink-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create Share Link'
        return context

class ShareLinkUpdateView(UpdateView):
    model = ShareLink
    fields = ['song', 'creator', 'email', 'perm']
    template_name = 'generic_form.html'
    success_url = reverse_lazy('sharelink-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update Share Link'
        return context

class ShareLinkDeleteView(DeleteView):
    model = ShareLink
    template_name = 'generic_confirm_delete.html'
    success_url = reverse_lazy('sharelink-list')
