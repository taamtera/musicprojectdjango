from django.db import models

class Song(models.Model):
    STATUS_CHOICES = [
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
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")
    description = models.TextField(blank=True)
    gen_status = models.CharField(max_length=50, choices=STATUS_CHOICES, default='in-progress')
    generation_method = models.CharField(max_length=10, choices=METHOD_CHOICES, default='mock')
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    generated_by = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='generated_songs')

    def __str__(self):
        return self.title
