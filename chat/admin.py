from django.contrib import admin

from .models import Message, Room


@admin.register(Room)
class RoomAdmin(admin.ModelAdmin):
    list_display = ("name", "slug", "created_by", "created_at")
    prepopulated_fields = {"slug": ("name",)}
    search_fields = ("name", "description")


@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ("room", "user", "short_content", "created_at")
    list_filter = ("room",)
    search_fields = ("content", "user__username")

    @admin.display(description="Content")
    def short_content(self, obj):
        return obj.content[:60]
