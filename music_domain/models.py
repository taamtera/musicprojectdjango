from django.db import models
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.username

class Artist(User):
    class Meta:
        verbose_name = 'Artist'
        verbose_name_plural = 'Artists'

class Enjoyer(User):
    listens_to = models.ManyToManyField('Song', related_name='listeners', blank=True)

    class Meta:
        verbose_name = 'Enjoyer'
        verbose_name_plural = 'Enjoyers'

class Song(models.Model):
    title = models.CharField(max_length=255)
    genre = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    gen_status = models.CharField(max_length=50) # Status of generation
    
    # Artist generates song
    generated_by = models.ForeignKey(Artist, on_delete=models.CASCADE, related_name='generated_songs')

    def __str__(self):
        return self.title

class Library(models.Model):
    # User has two one-to-one libraries based on the diagram: has generated, has shared
    user_generated = models.OneToOneField(User, on_delete=models.CASCADE, related_name='generated_library', null=True, blank=True)
    user_shared = models.OneToOneField(User, on_delete=models.CASCADE, related_name='shared_library', null=True, blank=True)

    def __str__(self):
        if self.user_generated:
            return f"Generated Library of {self.user_generated.username}"
        elif self.user_shared:
            return f"Shared Library of {self.user_shared.username}"
        return f"Library {self.id}"

class LibraryEntry(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='entries')
    song = models.ForeignKey(Song, on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=50, help_text="Type of the entry")

    def __str__(self):
        return f"Entry for '{self.song.title}' in {self.library}"

class ShareLink(models.Model):
    song = models.ForeignKey(Song, on_delete=models.CASCADE, related_name='share_links')
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name='created_share_links')
    email = models.EmailField()
    perm = models.CharField(max_length=50, help_text="Permissions (e.g., read, write)")

    def __str__(self):
        return f"Share Link by {self.creator.username} for {self.song.title} to {self.email}"
