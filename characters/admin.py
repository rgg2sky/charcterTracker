from django.contrib import admin
from .models import (
    Character,
    CharacterClass,
    CharacterRace,
    AssociationType,
    CharacterAssociation,
)

admin.site.register(CharacterClass)
admin.site.register(CharacterRace)
admin.site.register(AssociationType)
admin.site.register(CharacterAssociation)
admin.site.register(Character)