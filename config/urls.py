from django.contrib import admin
from django.urls import include, path

from chat import views as chat_views

urlpatterns = [
    path("admin/", admin.site.urls),
    path("accounts/signup/", chat_views.signup, name="signup"),
    path("accounts/", include("django.contrib.auth.urls")),
    path("", include("chat.urls")),
]
