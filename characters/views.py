from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from django.contrib import messages

from .forms import CharacterForm, CharacterAssociationForm
from .models import Character, CharacterAssociation
from collections import defaultdict

@login_required
def character_list(request):
    q = (request.GET.get("q") or "").strip()

    characters = Character.objects.filter(user=request.user)
    if q:
        characters = characters.filter(
            Q(char_name__icontains=q)
            | Q(char_origin__icontains=q)
            | Q(backstory_summary__icontains=q)
        )

    characters = characters.order_by("char_name")
    return render(request, "characters/character_list.html", {"characters": characters})

@login_required
def character_create(request):
    if request.method == "POST":
        form = CharacterForm(request.POST)
        if form.is_valid():
            character = form.save(commit=False)
            character.user = request.user
            character.save()
            return redirect("character_detail", character_id=character.character_id)
    else:
        form = CharacterForm()

    return render(request, "characters/character_form.html", {"form": form, "mode": "create"})

@login_required
def character_detail(request, character_id):
    character = get_object_or_404(Character, character_id=character_id, user=request.user)

    outgoing = (
        CharacterAssociation.objects
        .filter(from_character=character)
        .select_related("to_character", "relationship_type")
    )
    incoming = (
        CharacterAssociation.objects
        .filter(to_character=character)
        .select_related("from_character", "relationship_type")
    )

    grouped = defaultdict(list)

    for rel in outgoing:
        other = rel.to_character
        grouped[other].append(rel.relationship_type.relationship_type)

    for rel in incoming:
        other = rel.from_character
        grouped[other].append(rel.relationship_type.relationship_type)

    relationship_groups = [
        (other, sorted(set(types)))
        for other, types in grouped.items()
    ]
    relationship_groups.sort(key=lambda t: (t[0].char_name or "").lower())

    relationship_form = CharacterAssociationForm(user=request.user, from_character=character)

    return render(
        request,
        "characters/character_detail.html",
        {
            "character": character,
            "relationship_groups": relationship_groups,
            "relationship_form": relationship_form,
        },
    )

@login_required
def character_edit(request, character_id):
    character = get_object_or_404(Character, character_id=character_id, user=request.user)

    if request.method == "POST":
        form = CharacterForm(request.POST, instance=character)
        if form.is_valid():
            form.save()
            return redirect("character_detail", character_id=character.character_id)
    else:
        form = CharacterForm(instance=character)

    outgoing = (
        CharacterAssociation.objects
        .filter(from_character=character)
        .select_related("to_character", "relationship_type")
    )
    incoming = (
        CharacterAssociation.objects
        .filter(to_character=character)
        .select_related("from_character", "relationship_type")
    )

    relationships = []
    for rel in outgoing:
        relationships.append((rel.to_character, rel.relationship_type))
    for rel in incoming:
        relationships.append((rel.from_character, rel.relationship_type))

    relationships.sort(key=lambda t: (t[0].char_name or "").lower())

    relationship_form = CharacterAssociationForm(user=request.user, from_character=character)

    return render(
        request,
        "characters/character_form.html",
        {
            "form": form,
            "mode": "edit",
            "character": character,
            "relationships": relationships,
            "relationship_form": relationship_form,
        },
    )

@require_POST
@login_required
def relationship_add(request, character_id):
    character = get_object_or_404(Character, character_id=character_id, user=request.user)

    form = CharacterAssociationForm(request.POST, user=request.user, from_character=character)
    if form.is_valid():
        to_character = form.cleaned_data["to_character"]
        relationship_type = form.cleaned_data["relationship_type"]

        assoc, created = CharacterAssociation.objects.get_or_create(
            from_character=character,
            to_character=to_character,
            relationship_type=relationship_type,
        )

        if created:
            messages.success(request, "Relationship added.")
        else:
            messages.info(request, "That relationship already exists.")
    else:
        messages.error(request, "Please correct the form and try again.")

    return redirect("character_edit", character_id=character.character_id)