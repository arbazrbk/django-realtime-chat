from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render

from .forms import RoomForm
from .models import Room

HISTORY_LIMIT = 50


def signup(request):
    if request.user.is_authenticated:
        return redirect("chat:room_list")
    form = UserCreationForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        user = form.save()
        login(request, user)
        return redirect("chat:room_list")
    return render(request, "registration/signup.html", {"form": form})


@login_required
def room_list(request):
    form = RoomForm(request.POST or None)
    if request.method == "POST" and form.is_valid():
        room = form.save(commit=False)
        room.created_by = request.user
        room.save()
        return redirect(room)
    rooms = Room.objects.all()
    return render(request, "chat/room_list.html", {"rooms": rooms, "form": form})


@login_required
def room_detail(request, slug):
    room = get_object_or_404(Room, slug=slug)
    recent = room.messages.select_related("user").order_by("-created_at")[:HISTORY_LIMIT]
    return render(
        request,
        "chat/room_detail.html",
        {"room": room, "chat_messages": reversed(list(recent))},
    )
