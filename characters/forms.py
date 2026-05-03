from django import forms
from .models import Character


class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["char_name", "char_origin", "backstory_summary", "race", "char_class"]
        widgets = {
            "backstory_summary": forms.Textarea(attrs={"rows": 6}),
        }