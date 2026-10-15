from django import forms
from django.utils.text import slugify

from .models import Room


class RoomForm(forms.ModelForm):
    class Meta:
        model = Room
        fields = ["name", "description"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "e.g. python-help"}),
            "description": forms.TextInput(attrs={"placeholder": "What is this room about?"}),
        }

    def clean_name(self):
        name = self.cleaned_data["name"].strip()
        slug = slugify(name)
        if not slug:
            raise forms.ValidationError("Room name must contain letters or numbers.")
        if Room.objects.filter(slug=slug).exists():
            raise forms.ValidationError("A room with this name already exists.")
        return name
