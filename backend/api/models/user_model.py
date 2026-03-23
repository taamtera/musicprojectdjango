from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)
    listens_to = models.ManyToManyField('backend.Song', related_name='listeners', blank=True)

    def __str__(self):
        return self.username
