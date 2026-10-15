from channels.db import database_sync_to_async
from channels.generic.websocket import AsyncJsonWebsocketConsumer

from . import presence
from .models import Message, Room


class ChatConsumer(AsyncJsonWebsocketConsumer):
    """
    One connection per user per open room tab.

    Client -> server events:
        {"type": "message", "content": "..."}
        {"type": "typing", "is_typing": true}

    Server -> client events:
        {"type": "message", "message": {...}}
        {"type": "typing", "user": "...", "is_typing": bool}
        {"type": "presence", "users": [...]}
        {"type": "error", "error": "..."}
    """

    async def connect(self):
        self.user = self.scope["user"]
        if not self.user.is_authenticated:
            await self.close(code=4401)
            return

        self.room_slug = self.scope["url_route"]["kwargs"]["slug"]
        self.room = await self.get_room(self.room_slug)
        if self.room is None:
            await self.close(code=4404)
            return

        self.group_name = f"chat_{self.room_slug}"
        await self.channel_layer.group_add(self.group_name, self.channel_name)
        await self.accept()

        users = presence.join(self.room_slug, self.user.username)
        await self.broadcast({"type": "presence.update", "users": users})

    async def disconnect(self, code):
        if not hasattr(self, "group_name"):
            return
        users = presence.leave(self.room_slug, self.user.username)
        await self.broadcast({"type": "presence.update", "users": users})
        await self.channel_layer.group_discard(self.group_name, self.channel_name)

    async def receive_json(self, content, **kwargs):
        event_type = content.get("type")
        if event_type == "message":
            await self.handle_message(content)
        elif event_type == "typing":
            await self.broadcast(
                {
                    "type": "typing.update",
                    "user": self.user.username,
                    "is_typing": bool(content.get("is_typing")),
                }
            )
        else:
            await self.send_error("Unknown event type.")

    async def handle_message(self, content):
        text = str(content.get("content", "")).strip()
        if not text:
            await self.send_error("Message cannot be empty.")
            return
        if len(text) > Message.MAX_LENGTH:
            await self.send_error(f"Message is longer than {Message.MAX_LENGTH} characters.")
            return
        payload = await self.save_message(text)
        await self.broadcast({"type": "chat.message", "message": payload})

    # Group event handlers -------------------------------------------------

    async def chat_message(self, event):
        await self.send_json({"type": "message", "message": event["message"]})

    async def typing_update(self, event):
        if event["user"] == self.user.username:
            return
        await self.send_json(
            {"type": "typing", "user": event["user"], "is_typing": event["is_typing"]}
        )

    async def presence_update(self, event):
        await self.send_json({"type": "presence", "users": event["users"]})

    # Helpers --------------------------------------------------------------

    async def broadcast(self, event):
        await self.channel_layer.group_send(self.group_name, event)

    async def send_error(self, error):
        await self.send_json({"type": "error", "error": error})

    @database_sync_to_async
    def get_room(self, slug):
        return Room.objects.filter(slug=slug).first()

    @database_sync_to_async
    def save_message(self, text):
        message = Message.objects.create(room=self.room, user=self.user, content=text)
        return message.to_payload()
