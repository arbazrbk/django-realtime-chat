# Roadmap

Each unchecked item is a small, self-contained change that fits in one commit.
Items are worked on top to bottom. When an item is done it is checked off in
the same commit that implements it.

## Phase 1 — Foundations

- [x] Django project with Channels and Daphne
- [x] Room and Message models
- [x] WebSocket consumer with presence and typing events
- [x] Room list, room detail and signup views
- [x] Templates, WebSocket client and styles
- [x] Tests for models, views and consumer
- [x] GitHub Actions CI
- [ ] Add a `.env.example` file documenting all environment variables
- [ ] Load environment variables from a `.env` file with python-dotenv
- [ ] Add ruff configuration in `pyproject.toml` and fix any lint issues
- [ ] Run ruff in the CI workflow
- [ ] Add a `requirements-dev.txt` for development-only tools
- [ ] Add a pre-commit config running ruff and basic file checks
- [ ] Add a `Makefile`-style `tasks.py` or scripts section documenting common commands
- [ ] Configure Django logging with a readable console format
- [ ] Add a custom 404 page that matches the site layout
- [ ] Add a custom 500 page that matches the site layout
- [ ] Add a favicon and page meta description

## Phase 2 — Messaging

- [ ] Show date separators ("Today", "Yesterday", date) between messages
- [ ] Group consecutive messages from the same user
- [ ] Show relative timestamps ("2 min ago") with full date on hover
- [ ] Load older messages when scrolling to the top (paginated JSON endpoint)
- [ ] Add tests for the message history endpoint
- [ ] Show a "new messages" button when the user has scrolled up
- [ ] Render URLs in messages as safe clickable links
- [ ] Support basic markdown (bold, italic, inline code) with safe escaping
- [ ] Add tests for message formatting
- [ ] Allow users to edit their own messages
- [ ] Broadcast message edits in realtime and show an "edited" label
- [ ] Allow users to delete their own messages (soft delete)
- [ ] Broadcast message deletions in realtime
- [ ] Add consumer tests for edit and delete events
- [ ] Add emoji reactions to messages (model)
- [ ] Toggle reactions over WebSocket and broadcast counts
- [ ] Render reactions under messages in the UI
- [ ] Add tests for reactions
- [ ] Reply to a specific message (quoted preview)
- [ ] Highlight messages that @mention the current user
- [ ] Add tests for mentions parsing
- [ ] Rate-limit messages per user per connection
- [ ] Add tests for rate limiting
- [ ] Auto-grow the message textarea up to a maximum height
- [ ] Show a character counter near the limit
- [ ] Replace `alert()` errors with inline toast notifications

## Phase 3 — Rooms

- [ ] Show message count and last activity on the room list
- [ ] Sort rooms by recent activity
- [ ] Search rooms by name or description
- [ ] Add tests for room search and sorting
- [ ] Let the room creator edit name and description
- [ ] Let the room creator delete the room
- [ ] Add tests for room edit and delete permissions
- [ ] Private rooms visible only to members
- [ ] Invite users to a private room by username
- [ ] Join and leave room actions with membership model
- [ ] Add tests for private room access in views and consumer
- [ ] Room topic that can be changed and is broadcast live
- [ ] Pinned messages per room
- [ ] Show pinned messages panel in the room UI
- [ ] Add tests for pinned messages
- [ ] Track last-read message per user per room
- [ ] Show unread counts on the room list
- [ ] Add tests for unread tracking
- [ ] Room member list page

## Phase 4 — Users and profiles

- [ ] User profile model with display name and bio
- [ ] Profile page showing a user's info and recent rooms
- [ ] Edit profile page
- [ ] Avatar upload with size and type validation
- [ ] Generated initials avatar as a fallback
- [ ] Show avatars next to messages and in the online list
- [ ] Add tests for profiles and avatar validation
- [ ] User status (online, away, busy) shown in presence
- [ ] Mark users "away" after inactivity in the client
- [ ] Password change page
- [ ] Password reset flow using the console email backend
- [ ] Add tests for password change and reset
- [ ] Block a user (hide their messages for you)
- [ ] Add tests for blocking

## Phase 5 — Direct messages

- [ ] Direct conversation model between two users
- [ ] Start a direct message from a profile page
- [ ] Direct message consumer reusing chat logic
- [ ] Direct message list in the sidebar
- [ ] Unread badge for direct messages
- [ ] Add tests for direct messages

## Phase 6 — Notifications

- [ ] Notification model for mentions and direct messages
- [ ] Per-user notification WebSocket channel
- [ ] Notification dropdown in the top bar
- [ ] Mark notifications as read
- [ ] Browser notifications when the tab is hidden (opt-in)
- [ ] Play a short sound for new mentions (toggleable)
- [ ] Add tests for notifications

## Phase 7 — Search and files

- [ ] Search messages within a room
- [ ] Highlight search matches in results
- [ ] Jump to a message from search results
- [ ] Add tests for message search
- [ ] Upload images in chat with validation
- [ ] Show image previews and a lightbox
- [ ] Upload small files (PDF, text) with size limits
- [ ] Add tests for uploads

## Phase 8 — Moderation and admin

- [ ] Room moderators role
- [ ] Moderators can delete any message in their room
- [ ] Mute a user in a room for a duration
- [ ] Report a message
- [ ] Admin views for reports
- [ ] Banned words filter configurable in admin
- [ ] Add tests for moderation features
- [ ] Audit log of moderation actions

## Phase 9 — API

- [ ] Read-only JSON API for rooms
- [ ] JSON API for room messages with pagination
- [ ] Token authentication for the API
- [ ] API endpoint to post a message (broadcasts to WebSocket clients)
- [ ] Document the API in `docs/api.md`
- [ ] Add tests for the API

## Phase 10 — Scaling and reliability

- [ ] Redis-backed presence store when `REDIS_URL` is set
- [ ] Add tests for the presence store abstraction
- [ ] Heartbeat ping/pong to detect dead connections
- [ ] Resend missed messages after reconnect using last seen id
- [ ] Add PostgreSQL support via `DATABASE_URL`
- [ ] Add database indexes for message queries
- [ ] Health check endpoint for load balancers
- [ ] Serve static files with WhiteNoise
- [ ] Production security settings (HSTS, secure cookies) when DEBUG is off
- [ ] Add tests for production settings

## Phase 11 — Deployment

- [ ] Dockerfile for the app
- [ ] docker-compose with Redis and PostgreSQL
- [ ] Management command to seed demo rooms and users
- [ ] Deployment guide in `docs/deployment.md`
- [ ] Run tests against PostgreSQL and Redis in CI

## Phase 12 — Polish

- [ ] Keyboard shortcuts (Esc to cancel reply, Up to edit last message)
- [ ] Theme toggle (light / dark / system) remembered per user
- [ ] Accessibility pass: labels, focus states, ARIA live regions
- [ ] Loading skeletons for history
- [ ] Empty states for rooms, search and notifications
- [ ] Screenshots in the README
- [ ] Architecture overview in `docs/architecture.md`
- [ ] Contributing guide
- [ ] Changelog
- [ ] Tag release v1.0.0 in the changelog
