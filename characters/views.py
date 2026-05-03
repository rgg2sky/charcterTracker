from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render

from .forms import CharacterForm
from .models import Character
from .models import Character, CharacterAssociation


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
    return render(request, "characters/character_list.html", {"characters": characters, "q": q})


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
        .order_by("relationship_type__relationship_type", "to_character__char_name")
    )

    incoming = (
        CharacterAssociation.objects
        .filter(to_character=character)
        .select_related("from_character", "relationship_type")
        .order_by("relationship_type__relationship_type", "from_character__char_name")
    )

    return render(
        request,
        "characters/character_detail.html",
        {
            "character": character,
            "outgoing_relationships": outgoing,
            "incoming_relationships": incoming,
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

    return render(
        request,
        "characters/character_form.html",
        {"form": form, "mode": "edit", "character": character},
    )