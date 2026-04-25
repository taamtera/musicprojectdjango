import time
import threading
import requests
import os
from django.conf import settings
from django.core.files.base import ContentFile

def start_polling():
    """Starts the background polling thread."""
    # Prevent double execution in development (Django reloader)
    if os.environ.get('RUN_MAIN') != 'true':
        return

    thread = threading.Thread(target=poll_songs_loop, daemon=True)
    thread.start()

def poll_songs_loop():
    # Delay initial start to let the server boot up
    time.sleep(5)
    print("\n[Background Task] Starting song polling service...")
    
    # We import inside the function to avoid circular imports during app registry loading
    from backend.models import Song
    
    while True:
        try:
            # We check all songs in progress
            songs = Song.objects.filter(gen_status='in-progress')
            count = songs.count()
            
            if count > 0:
                print(f"\n[Background Task] Polling Cycle: {count} song(s) in progress")
                for song in songs:
                    if song.generation_method == 'mock':
                        print(f"[Background Task] Mock Mode: Downloading {song.title} from mock URL...")
                        if song.audio_url:
                            download_and_save_audio(song, song.audio_url)
                            song.gen_status = 'done'
                            song.save()
                    elif song.task_id:
                        check_song_status(song)
            
        except Exception as e:
            print(f"[Background Task] Error in polling loop: {str(e)}")
            
        time.sleep(30)

def check_song_status(song):
    url = f"https://api.sunoapi.org/api/v1/generate/record-info?taskId={song.task_id}"
    headers = {"Authorization": f"Bearer {settings.SUNO_API_TOKEN}"}

    try:
        response = requests.get(url, headers=headers, timeout=10)
        data = response.json()

        if response.status_code == 200 and data.get("code") == 200:
            result_data = data.get("data", {})
            api_status = result_data.get("status")
            
            song.gen_status_result = api_status

            if api_status == "SUCCESS":
                suno_data = result_data.get("response", {}).get("sunoData", [])
                if suno_data:
                    audio_url = suno_data[0].get("audioUrl")
                    if audio_url:
                        download_and_save_audio(song, audio_url)
                        song.gen_status = 'done'
                        print(f"[Background Task] SUCCESS: {song.title} downloaded.")
            
            elif api_status in ["CREATE_TASK_FAILED", "GENERATE_AUDIO_FAILED", "CALLBACK_EXCEPTION", "SENSITIVE_WORD_ERROR"]:
                song.gen_status = 'failed'
                print(f"[Background Task] FAILED: {song.title} ({api_status})")
            
            song.save()
        
    except Exception as e:
        print(f"[Background Task] Error checking {song.title}: {str(e)}")

def download_and_save_audio(song, audio_url):
    try:
        response = requests.get(audio_url, timeout=30)
        if response.status_code == 200:
            filename = f"{song.title.replace(' ', '_')}_{song.task_id}.mp3"
            song.audio_file.save(filename, ContentFile(response.content), save=False)
            song.audio_url = audio_url
    except Exception as e:
        print(f"[Background Task] Failed to download audio: {str(e)}")
