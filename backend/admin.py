from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User, Song, ShareLink

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'name', 'is_staff')
    filter_horizontal = ('listens_to',)
    fieldsets = UserAdmin.fieldsets + (
        (None, {'fields': ('name', 'listens_to')}),
    )

@admin.register(Song)
class SongAdmin(admin.ModelAdmin):
    list_display = ('title', 'genre', 'gen_status', 'generated_by', 'created_at')
    list_filter = ('genre', 'gen_status', 'created_at')
    search_fields = ('title', 'description')

@admin.register(ShareLink)
class ShareLinkAdmin(admin.ModelAdmin):
    list_display = ('song', 'creator', 'email', 'can_view', 'can_download', 'can_share_forward')
    list_filter = ('can_view', 'can_download', 'can_share_forward')
