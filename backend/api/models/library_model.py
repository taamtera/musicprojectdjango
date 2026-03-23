from django.db import models

class Library(models.Model):
    user_generated = models.OneToOneField('backend.User', on_delete=models.CASCADE, related_name='generated_library', null=True, blank=True)
    user_shared = models.OneToOneField('backend.User', on_delete=models.CASCADE, related_name='shared_library', null=True, blank=True)

    def __str__(self):
        if self.user_generated:
            return f"Generated Library of {self.user_generated.username}"
        elif self.user_shared:
            return f"Shared Library of {self.user_shared.username}"
        return f"Library {self.id}"

class LibraryEntry(models.Model):
    library = models.ForeignKey(Library, on_delete=models.CASCADE, related_name='entries')
    song = models.ForeignKey('backend.Song', on_delete=models.CASCADE)
    entry_type = models.CharField(max_length=50, help_text="Type of the entry")

    def __str__(self):
        return f"Entry for '{self.song.title}' in {self.library}"
