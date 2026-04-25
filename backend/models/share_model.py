from django.db import models

class ShareLink(models.Model):
    song = models.ForeignKey('backend.Song', on_delete=models.CASCADE, related_name='share_links')
    creator = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='created_share_links')
    email = models.EmailField()
    can_view = models.BooleanField(default=True)
    can_download = models.BooleanField(default=False)
    can_share_forward = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Share Link by {self.creator.username} for {self.song.title} to {self.email}"
