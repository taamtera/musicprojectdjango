from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Song, Library, LibraryEntry, ShareLink

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'is_staff')
    filter_horizontal = ('listens_to',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'listens_to')}),
    )

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'gen_status', 'generated_by')
    list_filter = ('genre', 'gen_status')
    search_fields = ('title', 'description')

@admin.register(Library)
class LibraryAdmin(admin.ModelAdmin):
    list_display = ('id', 'user_generated', 'user_shared')

@admin.register(LibraryEntry)
class LibraryEntryAdmin(admin.ModelAdmin):
    list_display = ('library', 'song', 'entry_type')
    list_filter = ('entry_type',)

@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ('song', 'creator', 'email', 'perm')
    list_filter = ('perm',)
