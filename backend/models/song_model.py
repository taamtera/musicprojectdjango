import uuid
from django.db import models

class Song(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('in-progress', 'In Progress'),
        ('done', 'Done'),
        ('failed', 'Failed'),
    ]
    
    METHOD_CHOICES = [
        ('mock', 'Mock API (Testing)'),
        ('suno', 'Real Suno API'),
    ]

    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    
    # Status and Method
    gen_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='pending')
    gen_status_result = models.CharField(max_length=100, blank=True, null=True)
    generation_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='mock')
    
    # External IDs and Storage
    task_id = models.CharField(max_length=255, blank=True, null=True)
    audio_url = models.URLField(blank=True, null=True)
    audio_file = models.FileField(upload_to='songs/', blank=True, null=True)
    
    # Callback Security
    callback_token = models.CharField(max_length=100, default=uuid.uuid4, unique=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    generated_by = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='generated_songs')

    def __str__(self):
        return self.title

    def delete(self, *args, **kwargs):
        # Delete the associated audio file if it exists
        if self.audio_file:
            self.audio_file.delete(save=False)
        super().delete(*args, **kwargs)
