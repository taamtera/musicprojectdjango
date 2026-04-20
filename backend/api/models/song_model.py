from django.db import models

class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    tags = models.CharField(max_length=255, blank=True, help_text="Comma separated tags")
    description = models.TextField(blank=True)
    gen_status = models.CharField(max_length=50)
    audio_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    generated_by = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='generated_songs')

    def __str__(self):
        return self.title
