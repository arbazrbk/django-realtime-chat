from django.contrib.auth import get_user_model
from django.test import TestCase

from chat.models import Message, Room


class RoomModelTests(TestCase):
    def test_slug_is_generated_from_name(self):
        room = Room.objects.create(name="Python Help")
        self.assertEqual(room.slug, "python-help")

    def test_explicit_slug_is_kept(self):
        room = Room.objects.create(name="General", slug="lobby")
        self.assertEqual(room.slug, "lobby")

    def test_absolute_url_uses_slug(self):
        room = Room.objects.create(name="General")
        self.assertEqual(room.get_absolute_url(), "/rooms/general/")


class MessageModelTests(TestCase):
    def test_payload_contains_public_fields(self):
        user = get_user_model().objects.create_user("alice", password="pw-12345!")
        room = Room.objects.create(name="General")
        message = Message.objects.create(room=room, user=user, content="hi")

        payload = message.to_payload()

        self.assertEqual(payload["id"], message.id)
        self.assertEqual(payload["user"], "alice")
        self.assertEqual(payload["content"], "hi")
        self.assertIn("created_at", payload)
