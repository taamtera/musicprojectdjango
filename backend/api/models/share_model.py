from django.db import models

class ShareLink(models.Model):
    song = models.ForeignKey('backend.Song', on_delete=models.CASCADE, related_name='share_links')
    creator = models.ForeignKey('backend.User', on_delete=models.CASCADE, related_name='created_share_links')
    email = models.EmailField()
    perm = models.CharField(max_length=50, help_text="Permissions (e.g., read, write)")

    def __str__(self):
        return f"Share Link by {self.creator.username} for {self.song.title} to {self.email}"
