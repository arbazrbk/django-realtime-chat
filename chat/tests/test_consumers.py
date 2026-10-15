from channels.db import database_sync_to_async
from channels.routing import URLRouter
from channels.testing import WebsocketCommunicator
from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.test import TransactionTestCase

from chat import presence
from chat.models import Message, Room
from chat.routing import websocket_urlpatterns

application = URLRouter(websocket_urlpatterns)


class ChatConsumerTests(TransactionTestCase):
    def setUp(self):
        presence.reset()
        User = get_user_model()
        self.alice = User.objects.create_user("alice", password="pw-12345!")
        self.bob = User.objects.create_user("bob", password="pw-12345!")
        self.room = Room.objects.create(name="General")

    async def connect(self, user, slug="general"):
        communicator = WebsocketCommunicator(application, f"/ws/rooms/{slug}/")
        communicator.scope["user"] = user
        connected, code = await communicator.connect()
        return communicator, connected, code

    async def test_anonymous_user_is_rejected(self):
        _, connected, code = await self.connect(AnonymousUser())
        self.assertFalse(connected)
        self.assertEqual(code, 4401)

    async def test_unknown_room_is_rejected(self):
        _, connected, code = await self.connect(self.alice, slug="missing")
        self.assertFalse(connected)
        self.assertEqual(code, 4404)

    async def test_presence_is_broadcast_on_join_and_leave(self):
        alice, connected, _ = await self.connect(self.alice)
        self.assertTrue(connected)
        self.assertEqual(await alice.receive_json_from(), {"type": "presence", "users": ["alice"]})

        bob, _, _ = await self.connect(self.bob)
        expected = {"type": "presence", "users": ["alice", "bob"]}
        self.assertEqual(await alice.receive_json_from(), expected)
        self.assertEqual(await bob.receive_json_from(), expected)

        await bob.disconnect()
        self.assertEqual(await alice.receive_json_from(), {"type": "presence", "users": ["alice"]})
        await alice.disconnect()

    async def test_message_is_saved_and_broadcast(self):
        alice, _, _ = await self.connect(self.alice)
        bob, _, _ = await self.connect(self.bob)
        await alice.receive_json_from()
        await alice.receive_json_from()
        await bob.receive_json_from()

        await alice.send_json_to({"type": "message", "content": "  hello bob  "})

        for communicator in (alice, bob):
            event = await communicator.receive_json_from()
            self.assertEqual(event["type"], "message")
            self.assertEqual(event["message"]["user"], "alice")
            self.assertEqual(event["message"]["content"], "hello bob")

        count = await database_sync_to_async(Message.objects.filter(room=self.room).count)()
        self.assertEqual(count, 1)
        await alice.disconnect()
        await bob.disconnect()

    async def test_empty_message_returns_error(self):
        alice, _, _ = await self.connect(self.alice)
        await alice.receive_json_from()

        await alice.send_json_to({"type": "message", "content": "   "})

        self.assertEqual(
            await alice.receive_json_from(),
            {"type": "error", "error": "Message cannot be empty."},
        )
        await alice.disconnect()

    async def test_typing_event_is_not_echoed_to_sender(self):
        alice, _, _ = await self.connect(self.alice)
        bob, _, _ = await self.connect(self.bob)
        await alice.receive_json_from()
        await alice.receive_json_from()
        await bob.receive_json_from()

        await alice.send_json_to({"type": "typing", "is_typing": True})

        self.assertEqual(
            await bob.receive_json_from(),
            {"type": "typing", "user": "alice", "is_typing": True},
        )
        self.assertTrue(await alice.receive_nothing())
        await alice.disconnect()
        await bob.disconnect()
