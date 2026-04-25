from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from backend.models import ShareLink

class ShareLinkListView(LoginRequiredMixin, ListView):
    model = ShareLink
    template_name = 'frontend/sharelink_list.html'

    def get_queryset(self):
        # Only show shares created by the current user
        queryset = ShareLink.objects.filter(creator=self.request.user)
        
        from django.db.models import Q
        sort_by = self.request.GET.get('sort', '-created_at')
        query = self.request.GET.get('title', '')
        
        if query:
            queryset = queryset.filter(
                Q(song__title__icontains=query) | 
                Q(song__genre__icontains=query) | 
                Q(song__description__icontains=query)
            )
            
        if sort_by in ['created_at', '-created_at']:
            queryset = queryset.order_by(sort_by)
        elif sort_by == 'title':
            queryset = queryset.order_by('song__title')
        elif sort_by == '-title':
            queryset = queryset.order_by('-song__title')
            
        return queryset

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
