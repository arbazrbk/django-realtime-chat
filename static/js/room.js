(function () {
  "use strict";

  const roomSlug = JSON.parse(document.getElementById("room-slug").textContent);
  const currentUser = JSON.parse(document.getElementById("current-user").textContent);

  const messagesEl = document.getElementById("messages");
  const form = document.getElementById("message-form");
  const input = document.getElementById("message-input");
  const statusEl = document.getElementById("status");
  const typingEl = document.getElementById("typing");
  const onlineEl = document.getElementById("online-users");

  const typingUsers = new Map();
  let socket = null;
  let retryDelay = 1000;
  let typingTimeout = null;
  let isTyping = false;

  function setStatus(state, label) {
    statusEl.className = "status status-" + state;
    statusEl.textContent = label;
  }

  function formatTime(iso) {
    return new Date(iso).toLocaleTimeString([], { hour: "2-digit", minute: "2-digit" });
  }

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function appendMessage(message) {
    const li = document.createElement("li");
    li.className = "message" + (message.user === currentUser ? " own" : "");

    const author = document.createElement("span");
    author.className = "author";
    author.textContent = message.user;

    const time = document.createElement("time");
    time.dateTime = message.created_at;
    time.textContent = formatTime(message.created_at);

    const body = document.createElement("p");
    body.textContent = message.content;

    li.append(author, time, body);
    messagesEl.appendChild(li);
    scrollToBottom();
  }

  function renderOnline(users) {
    onlineEl.replaceChildren(
      ...users.map(function (name) {
        const li = document.createElement("li");
        li.textContent = name + (name === currentUser ? " (you)" : "");
        return li;
      })
    );
  }

  function renderTyping() {
    const names = Array.from(typingUsers.keys());
    if (names.length === 0) typingEl.textContent = "";
    else if (names.length === 1) typingEl.textContent = names[0] + " is typing…";
    else typingEl.textContent = names.join(", ") + " are typing…";
  }

  function handleTyping(user, active) {
    clearTimeout(typingUsers.get(user));
    if (active) {
      // Drop the indicator if the "stopped typing" event never arrives.
      typingUsers.set(user, setTimeout(function () {
        typingUsers.delete(user);
        renderTyping();
      }, 5000));
    } else {
      typingUsers.delete(user);
    }
    renderTyping();
  }

  function send(data) {
    if (socket && socket.readyState === WebSocket.OPEN) {
      socket.send(JSON.stringify(data));
      return true;
    }
    return false;
  }

  function setTyping(active) {
    if (isTyping === active) return;
    isTyping = active;
    send({ type: "typing", is_typing: active });
  }

  function connect() {
    const scheme = window.location.protocol === "https:" ? "wss" : "ws";
    socket = new WebSocket(scheme + "://" + window.location.host + "/ws/rooms/" + roomSlug + "/");

    socket.addEventListener("open", function () {
      retryDelay = 1000;
      setStatus("online", "Connected");
    });

    socket.addEventListener("message", function (event) {
      const data = JSON.parse(event.data);
      switch (data.type) {
        case "message":
          handleTyping(data.message.user, false);
          appendMessage(data.message);
          break;
        case "typing":
          handleTyping(data.user, data.is_typing);
          break;
        case "presence":
          renderOnline(data.users);
          break;
        case "error":
          window.alert(data.error);
          break;
      }
    });

    socket.addEventListener("close", function (event) {
      if (event.code === 4401 || event.code === 4404) {
        setStatus("offline", "Disconnected");
        return;
      }
      setStatus("connecting", "Reconnecting…");
      setTimeout(connect, retryDelay);
      retryDelay = Math.min(retryDelay * 2, 30000);
    });
  }

  form.addEventListener("submit", function (event) {
    event.preventDefault();
    const content = input.value.trim();
    if (!content) return;
    if (send({ type: "message", content: content })) {
      input.value = "";
      setTyping(false);
    }
  });

  input.addEventListener("keydown", function (event) {
    if (event.key === "Enter" && !event.shiftKey) {
      event.preventDefault();
      form.requestSubmit();
    }
  });

  input.addEventListener("input", function () {
    setTyping(input.value.trim().length > 0);
    clearTimeout(typingTimeout);
    typingTimeout = setTimeout(function () { setTyping(false); }, 3000);
  });

  scrollToBottom();
  connect();
})();
