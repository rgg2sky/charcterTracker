from django import forms
from .models import Character, CharacterAssociation

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["char_name", "char_origin", "backstory_summary", "race", "char_class"]
        widgets = {
            "backstory_summary": forms.Textarea(attrs={"rows": 6}),
        }

class CharacterAssociationForm(forms.ModelForm):
    class Meta:
        model = CharacterAssociation
        fields = ["to_character", "relationship_type"]

    def __init__(self, *args, user=None, from_character=None, **kwargs):
        super().__init__(*args, **kwargs)

        # Only allow linking to characters owned by this user
        if user is not None:
            self.fields["to_character"].queryset = Character.objects.filter(user=user).order_by("char_name")

        # Prevent selecting self
        if from_character is not None:
            self.fields["to_character"].queryset = self.fields["to_character"].queryset.exclude(
                character_id=from_character.character_id
            )