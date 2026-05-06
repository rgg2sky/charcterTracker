from django import forms
from .models import Character, CharacterAssociation

class CharacterForm(forms.ModelForm):
    class Meta:
        model = Character
        fields = ["char_name", "char_origin", "backstory_summary", "race", "char_class"]
        widgets = {
            "backstory_summary": forms.Textarea(attrs={"rows": 6}),
        }

class CharacterAssociationForm(forms.ModelForm): #form for creating/editing character relationships
    class Meta:
        model = CharacterAssociation
        fields = ["to_character", "relationship_type"]

    def __init__(self, *args, user=None, from_character=None, **kwargs):
        super().__init__(*args, **kwargs)

        if user is not None: #used for filtering the character list to only show the users characters
            self.fields["to_character"].queryset = Character.objects.filter(user=user).order_by("char_name")

        if from_character is not None: #used to prevent linking a character to itself
            self.fields["to_character"].queryset = self.fields["to_character"].queryset.exclude(
                character_id=from_character.character_id
            )