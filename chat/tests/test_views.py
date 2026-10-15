from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from chat.models import Message, Room


class ViewTests(TestCase):
    def setUp(self):
        self.user = get_user_model().objects.create_user("alice", password="pw-12345!")

    def test_room_list_requires_login(self):
        response = self.client.get(reverse("chat:room_list"))
        self.assertEqual(response.status_code, 302)
        self.assertIn(reverse("login"), response["Location"])

    def test_room_list_shows_rooms(self):
        Room.objects.create(name="General")
        self.client.force_login(self.user)
        response = self.client.get(reverse("chat:room_list"))
        self.assertContains(response, "# General")

    def test_create_room_redirects_to_room(self):
        self.client.force_login(self.user)
        response = self.client.post(
            reverse("chat:room_list"), {"name": "Django Tips", "description": ""}
        )
        room = Room.objects.get(slug="django-tips")
        self.assertRedirects(response, room.get_absolute_url())
        self.assertEqual(room.created_by, self.user)

    def test_duplicate_room_name_is_rejected(self):
        Room.objects.create(name="General")
        self.client.force_login(self.user)
        response = self.client.post(reverse("chat:room_list"), {"name": "general"})
        self.assertEqual(response.status_code, 200)
        self.assertEqual(Room.objects.count(), 1)

    def test_room_detail_shows_recent_history(self):
        room = Room.objects.create(name="General")
        Message.objects.create(room=room, user=self.user, content="hello there")
        self.client.force_login(self.user)
        response = self.client.get(room.get_absolute_url())
        self.assertContains(response, "hello there")

    def test_unknown_room_returns_404(self):
        self.client.force_login(self.user)
        response = self.client.get(reverse("chat:room_detail", args=["missing"]))
        self.assertEqual(response.status_code, 404)

    def test_signup_creates_user_and_logs_in(self):
        response = self.client.post(
            reverse("signup"),
            {"username": "bob", "password1": "S3cure-pass!", "password2": "S3cure-pass!"},
        )
        self.assertRedirects(response, reverse("chat:room_list"))
        self.assertTrue(get_user_model().objects.filter(username="bob").exists())
