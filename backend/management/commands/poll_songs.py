import time
import requests
from django.core.management.base import BaseCommand
from django.conf import settings
from django.core.files.base import ContentFile
from backend.models import Song

class Command(BaseCommand):
    help = 'Poll Suno API for song status and download finished files'

    def handle(self, *args, **options):
        self.stdout.write(self.style.SUCCESS("Starting song polling service..."))
        
        while True:
            songs = Song.objects.filter(gen_status='in-progress', task_id__isnull=False)
            count = songs.count()
            
            self.stdout.write(self.style.MIGRATE_HEADING(f"\n--- Polling Cycle: {count} song(s) in progress ---"))
            
            if count == 0:
                self.stdout.write("Status: Idle. No songs to check.")
            else:
                for song in songs:
                    status_display = song.gen_status_result or "PENDING"
                    self.stdout.write(f"Checking: {song.title} | Task ID: {song.task_id} | Status: {status_display}")
                    self.check_song_status(song)
            
            self.stdout.write(self.style.MIGRATE_HEADING("--- Cycle Complete (Waiting 30s) ---\n"))
            time.sleep(30)

    def check_song_status(self, song):
        url = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={song.task_id}"
        headers = {
            "Authorization": f"Bearer {settings.SUNO_API_TOKEN}"
        }

        try:
            response = requests.get(url, headers=headers, timeout=10)
            data = response.json()

            if response.status_code == 200 and data.get("code") == 200:
                result_data = data.get("data", {})
                api_status = result_data.get("status")
                
                # Save the raw status from API
                song.gen_status_result = api_status

                if api_status == "SUCCESS":
                    suno_data = result_data.get("response", {}).get("sunoData", [])
                    if suno_data:
                        audio_url = suno_data[0].get("audioUrl")
                        if audio_url:
                            self.stdout.write(f"Download started for: {song.title}")
                            self.download_and_save_audio(song, audio_url)
                            song.gen_status = 'done'
                            self.stdout.write(self.style.SUCCESS(f"Successfully updated: {song.title}"))
                
                elif api_status in ["CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED", "CALLBACK_EXCEPTION", "SENSITIVE_WORD_ERROR"]:
                    song.gen_status = 'failed'
                    self.stdout.write(self.style.ERROR(f"Generation failed ({api_status}) for: {song.title}"))
                
                elif api_status in ["PENDING", "TEXT_SUCCESS", "FIRST_SUCCESS"]:
                    # Still in progress, just save the updated gen_status_result
                    self.stdout.write(f"Song {song.title} is currently: {api_status}")
                
                song.save()
            
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Error checking {song.title}: {str(e)}"))

    def download_and_save_audio(self, song, audio_url):
        try:
            response = requests.get(audio_url, timeout=30)
            if response.status_code == 200:
                # Generate a filename
                filename = f"{song.title.replace(' ', '_')}_{song.task_id}.mp3"
                song.audio_file.save(filename, ContentFile(response.content), save=False)
                song.audio_url = audio_url # Also update the URL field
        except Exception as e:
            self.stdout.write(self.style.ERROR(f"Failed to download audio: {str(e)}"))
