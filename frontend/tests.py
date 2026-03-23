from django.test import TestCase
from django.urls import reverse
from backend.models import User, Song

class ConsolidatedAppsTest(TestCase):
    def setUp(self):
        self.user = User.objects.create(
            username="testuser", 
            email="user@example.com", 
            name="Test User"
        )
        self.song = Song.objects.create(
            title="Consolidated Test Song",
            genre="Pop",
            description="Testing the new backend/frontend.",
            gen_status="completed",
            generated_by=self.user
        )

    def test_database_model_creation(self):
        self.assertEqual(Song.objects.count(), 1)
        self.assertEqual(User.objects.count(), 1)
        self.assertEqual(self.song.generated_by.username, "testuser")

    def test_frontend_routing_responds_200(self):
        url = reverse('song-list')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Consolidated Test Song")
