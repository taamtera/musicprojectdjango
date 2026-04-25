from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from backend.models import User

class UserListView(LoginRequiredMixin, ListView):
    model = User
    template_name = 'users/list.html'

class UserCreateView(LoginRequiredMixin, CreateView):
    model = User
    fields = ['username', 'email', 'name', 'is_staff']
    template_name = 'common/form.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Create User'
        return context

class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = User
    fields = ['username', 'email', 'name', 'is_staff']
    template_name = 'common/form.html'
    success_url = reverse_lazy('user-list')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['title'] = 'Update User'
        return context

class UserDeleteView(LoginRequiredMixin, DeleteView):
    model = User
    template_name = 'common/confirm_delete.html'
    success_url = reverse_lazy('user-list')
