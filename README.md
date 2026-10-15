# Django Realtime Chat

[![Tests](https://github.com/arbazrbk/django-realtime-chat/actions/workflows/tests.yml/badge.svg)](https://github.com/arbazrbk/django-realtime-chat/actions/workflows/tests.yml)

A realtime chat application built with **Django** and **Django Channels**. Users sign up, create rooms and chat over WebSockets with live presence and typing indicators.

## Features

- Account sign up, log in and log out
- Create and browse chat rooms
- Realtime messaging over WebSockets
- Message history (last 50 messages on page load)
- Online users list per room
- "User is typing…" indicator
- Automatic reconnect with exponential backoff
- Responsive layout with dark mode

## Tech stack

| Layer      | Tools                                  |
|------------|----------------------------------------|
| Backend    | Django, Django Channels, Daphne (ASGI)  |
| Realtime   | WebSockets, channel layers (in-memory or Redis) |
| Frontend   | Django templates, vanilla JavaScript, CSS |
| Database   | SQLite (development)                   |
| CI         | GitHub Actions                         |

## Getting started

```bash
git clone https://github.com/arbazrbk/django-realtime-chat.git
cd django-realtime-chat

python -m venv .venv
# Windows: .venv\Scripts\activate
source .venv/bin/activate

pip install -r requirements.txt
python manage.py migrate
python manage.py createsuperuser   # optional, for /admin
python manage.py runserver
```

Open http://127.0.0.1:8000, create an account and start a room. Open the same room in a second browser (or a private window with another account) to see messages arrive in realtime.

`runserver` is served by Daphne, so WebSockets work out of the box.

## Configuration

| Variable               | Default                  | Purpose                                   |
|------------------------|--------------------------|-------------------------------------------|
| `DJANGO_SECRET_KEY`    | development key          | Secret key; **set this in production**    |
| `DJANGO_DEBUG`         | `true`                   | Debug mode                                |
| `DJANGO_ALLOWED_HOSTS` | `localhost,127.0.0.1`    | Comma-separated allowed hosts             |
| `REDIS_URL`            | unset                    | Use Redis as the channel layer when set   |

Without `REDIS_URL` the in-memory channel layer is used, which only works with a single server process.

## WebSocket protocol

Connect to `/ws/rooms/<slug>/` while logged in.

Client → server:

```json
{"type": "message", "content": "Hello!"}
{"type": "typing", "is_typing": true}
```

Server → client:

```json
{"type": "message", "message": {"id": 1, "user": "alice", "content": "Hello!", "created_at": "..."}}
{"type": "typing", "user": "alice", "is_typing": true}
{"type": "presence", "users": ["alice", "bob"]}
{"type": "error", "error": "Message cannot be empty."}
```

Close codes: `4401` not authenticated, `4404` room not found.

## Running tests

```bash
python manage.py test
```

## Project structure

```
config/          Django settings, URLs, ASGI entrypoint
chat/            Models, views, forms, WebSocket consumer, routing, tests
templates/       Base layout, auth pages and chat pages
static/          CSS and the WebSocket client
```

## Roadmap

See [ROADMAP.md](ROADMAP.md) for planned features.

## License

[MIT](LICENSE)
