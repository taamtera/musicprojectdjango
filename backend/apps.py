from django.apps import AppConfig


class BackendConfig(AppConfig):
    default_auto_field = 'django_mongodb_backend.fields.ObjectIdAutoField'
    name = 'backend'

    def ready(self):
        from .tasks import start_polling
        start_polling()
