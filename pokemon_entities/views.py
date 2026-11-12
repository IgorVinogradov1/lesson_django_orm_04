import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from pokemon_entities.models import Pokemon, PokemonEntity
from django.utils import timezone
from django.shortcuts import render, get_object_or_404


MOSCOW_CENTER = [55.751244, 37.618423]


def show_all_pokemons(request):
    current_time = timezone.now()
    pokemon_markers = []
    for pokemon in Pokemon.objects.all():
        img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None
        active_pokemons = PokemonEntity.objects.filter(pokemon=pokemon).exclude(appeared_at__gte=current_time).exclude(disappeared_at__lte=current_time)
        for pokemon_entity in active_pokemons:
            pokemon_markers.append({
                "lat": pokemon_entity.lat,
                "lon": pokemon_entity.lon,
                "image_url": img_url,
            })   

    pokemons_on_page = []
    for pokemon in Pokemon.objects.all():
        img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None
        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': img_url,
            'title_ru': pokemon.title_ru,
        })

    return render(request, 'mainpage.html', context={
        'pokemons': pokemons_on_page,
        'pokemon_markers': pokemon_markers,
        'moscow_center': MOSCOW_CENTER,
    })


def show_pokemon(request, pokemon_id):
    pokemon = get_object_or_404(Pokemon, id=pokemon_id)
    img_url = request.build_absolute_uri(pokemon.photo.url) if pokemon.photo else None

    current_time = timezone.now()
    pokemon_markers = []
    active_pokemons = PokemonEntity.objects.filter(pokemon=pokemon).exclude(appeared_at__gte=current_time).exclude(disappeared_at__lte=current_time)
    for pokemon_entity in active_pokemons:
        pokemon_markers.append({
            "lat": pokemon_entity.lat,
            "lon": pokemon_entity.lon,
            "image_url": img_url,
        })

    requested_pokemon = {
        'img_url': img_url,
        'title_ru': pokemon.title_ru,
        'title_en': pokemon.title_en,
        'title_jp': pokemon.title_jp,
        'description': pokemon.description,
        'entities': pokemon_markers,
    }

    return render(request, 'pokemon.html', context={
        'pokemon': requested_pokemon,
        'moscow_center': MOSCOW_CENTER,
    })