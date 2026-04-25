from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy


class LandingLoginRequiredMixin(LoginRequiredMixin):
    """Redirect unauthenticated users directly to landing page."""

    login_url = reverse_lazy('index')
    redirect_field_name = None
