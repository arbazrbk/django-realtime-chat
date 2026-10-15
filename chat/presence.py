"""
Tracks which users are connected to each room.

This is an in-process store, so it is only accurate for a single server
process. A Redis-backed implementation is on the roadmap.
"""

from collections import Counter, defaultdict

_connections = defaultdict(Counter)


def join(room_slug, username):
    _connections[room_slug][username] += 1
    return online_users(room_slug)


def leave(room_slug, username):
    room = _connections[room_slug]
    room[username] -= 1
    if room[username] <= 0:
        del room[username]
    if not room:
        _connections.pop(room_slug, None)
    return online_users(room_slug)


def online_users(room_slug):
    return sorted(_connections.get(room_slug, {}))


def reset():
    _connections.clear()
