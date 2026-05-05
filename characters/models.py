from django.db import models
from django.contrib.auth.models import User

class CharacterClass(models.Model):
    """Represents D&D character classes"""
    char_class_id = models.AutoField(primary_key=True)
    char_class_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'character_class'
        verbose_name_plural = "Character Classes"
    
    def __str__(self):
        return self.char_class_name


class CharacterRace(models.Model):
    """Represents D&D character races"""
    char_race_id = models.AutoField(primary_key=True)
    char_race_name = models.CharField(max_length=100, unique=True)
    
    class Meta:
        db_table = 'character_race'
    
    def __str__(self):
        return self.char_race_name


class Character(models.Model):
    """Represents a user's character"""
    character_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='characters')
    char_name = models.CharField(max_length=100)
    char_origin = models.CharField(max_length=255, blank=True, null=True)
    backstory_summary = models.TextField(blank=True, null=True)
    race = models.ForeignKey(CharacterRace, on_delete=models.SET_NULL, null=True)
    char_class = models.ForeignKey(CharacterClass, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'character'
    
    def __str__(self):
        return self.char_name


class AssociationType(models.Model):
    """Types of relationships between characters"""
    relationship_type_id = models.AutoField(primary_key=True)
    relationship_type = models.CharField(max_length=100, unique=True)

    inverse_type = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="inverse_of",
    )

    class Meta:
        db_table = 'association_type'

    def __str__(self):
        return self.relationship_type


class CharacterAssociation(models.Model):
    """Relationships between characters"""
    from_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='associations_from')
    to_character = models.ForeignKey(Character, on_delete=models.CASCADE, related_name='associations_to')
    relationship_type = models.ForeignKey(AssociationType, on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'character_association'
        unique_together = ('from_character', 'to_character', 'relationship_type')
    
    def __str__(self):
        return f"{self.from_character} -> {self.to_character} ({self.relationship_type})"
